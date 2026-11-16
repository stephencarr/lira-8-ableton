// Embedded in v8.codebox. Native LiveAPI only; no files, network or externals.
inlets = 1;
outlets = 4; // 0: saved controls, 1: temporary tuning modifier, 2: status, 3: DSP state sync
var surface = null, self = null, song = null, appAPI = null, trackView = null;
var controls = [], grabbed = [], active = false, ready = false, enabled = true;
var voices = [0,0,0,0,0,0,0,0], pageIndex = 0, queue = [];
var levels = [127,127,127,127,127,127,127,127];
var parameterRefs=[], surfaceSlot=-1;
var hasShift=false, shiftBinding=null;
var lastStatus = '', ticks = 0, discoveredCount = 0, redrawTicks = 0;
// Existing Push palette: muted sage, blue-grey, lavender, mauve.
var PAIRS = [53,55,57,59];
var PAGES = [{"name": "Voices 1-2", "parameters": ["Tune 1", "Tune 2", "FM 12", "Sharp 12", "Source 12", "Fast 12", "Pitch 1234", "Hold 1234"]}, {"name": "Voices 3-4", "parameters": ["Tune 3", "Tune 4", "FM 34", "Sharp 34", "Source 34", "Fast 34", "Pitch 1234", "Hold 1234"]}, {"name": "Voices 5-6", "parameters": ["Tune 5", "Tune 6", "FM 56", "Sharp 56", "Source 56", "Fast 56", "Pitch 5678", "Hold 5678"]}, {"name": "Voices 7-8", "parameters": ["Tune 7", "Tune 8", "FM 78", "Sharp 78", "Source 78", "Fast 78", "Pitch 5678", "Hold 5678"]}, {"name": "Hyper LFO", "parameters": ["LFO A", "LFO B", "LFO AND OR", "LFO Link", "Vibrato", "Quantize", "FM Routing", "Total FB"]}, {"name": "Delay", "parameters": ["Delay Time 1", "Delay Time 2", "Delay Mod 1", "Delay Mod 2", "Feedback", "Delay Mix", "Delay Source", "Delay Wave"]}, {"name": "Output", "parameters": ["Drive", "Dist Mix", "Master", "Audio In", "Audio From", "Audio Tap", "Delay Mix", "Pad Control"]}, {"name": "Voice Mixer", "parameters": ["Voice 1 Level", "Voice 2 Level", "Voice 3 Level", "Voice 4 Level", "Voice 5 Level", "Voice 6 Level", "Voice 7 Level", "Voice 8 Level"]}];
var work = new Task(flush, this);
var clock = new Task(tick, this);
clock.interval = 250;
function status(s) {
 var n=/Pads ready/.test(s)?6:/Pads off/.test(s)?1:/Select LIRA/.test(s)?2:/No pad matrix/.test(s)?4:/Press Note/.test(s)?5:/Waiting for Push/.test(s)?3:/error|failed|Reconnecting/.test(s)?7:0;
 outlet(0,'padstatusvalue',n);
 if (s !== lastStatus) { lastStatus=s; outlet(2, 'set', s); post('LIRA Pads: '+s+'\n'); } }
function idOf(value) {
 var a = Array.isArray(value) ? value : [value];
 for(var i=0;i<a.length;i++) if(a[i]==='id') return Number(a[i+1]);
 return Number(a[0]) || 0;
}
// Control-surface/proxy IDs may be negative. Only zero is the null ID.
function ids(value) {
 var a=Array.isArray(value)?value:[value], result=[];
 for(var i=0;i<a.length;i++) if(isFinite(Number(a[i])) && Number(a[i])!==0) result.push(Number(a[i]));
 return result;
}
function api(id) { return new LiveAPI(null, 'id '+id); }
function schedule(action) { queue.push(action); work.schedule(1); }
function flush() {
 var jobs=queue; queue=[];
 for(var i=0;i<jobs.length;i++) {
  try { jobs[i](); } catch(e) { release(); status('Pad error: '+e.message); }
 }
}
function init() {
 shutdown(); ticks=0; lastStatus="";
 try {
  self=new LiveAPI(null,'this_device'); song=new LiveAPI(null,'live_set'); appAPI=new LiveAPI(null,'live_app'); trackView=new LiveAPI(null,'live_set view selected_track view');
  if(!self.id) { status('Waiting for Live'); return; }
  ready=true; bindstate(); clock.repeat(); tick();
 } catch(e) { status('Init error: '+e.message); }
}
function enable(v) { enabled=Number(v)>0; if(!enabled) release(); if(ready) schedule(tick); }
function state(i,v) { i=Number(i); if(i<0||i>7)return; voices[i]=Number(v)>0?1:0; if(active) schedule(redraw); }
function level(i,v) { i=Number(i); if(i<0||i>7)return; levels[i]=Math.max(0,Math.min(127,Number(v)||0)); if(active)schedule(redraw); }
function page(v) {
 var n=Math.max(0,Math.min(7,Math.round(Number(v)||0)));
 pageIndex=n;
 if(ready) schedule(function(){applypage();paint();});
}
function applypage() {
 // Recovery: native bank selection only. The previous API request caused
 // a reported Push reboot. Never call it from a pad or restored parameter.
 status('Use display buttons to select banks');
}
function acceptstate(ref,value){
 var v=Number(Array.isArray(value)?value[0]:value);
 if(!isFinite(v))return;
 if(ref.kind==='level') {level(ref.index,v);outlet(3,'level'+(ref.index+1),v);}
 else state(ref.index,v);
}
function statecallback(ref){return function(a){if(a&&a[0]==='value')schedule(function(){acceptstate(ref,a[1]);});};}
function bindstate(){
 for(var i=0;i<parameterRefs.length;i++)try{parameterRefs[i].api.property='';}catch(e){}
 parameterRefs=[];
 var all=ids(self.get('parameters'));
 for(var j=0;j<all.length;j++){
  var p=api(all[j]),name=String(p.get('name')),m=/^Voice ([1-8]) (Level|On)$/.exec(name);
  if(!m)continue;
  var r={index:Number(m[1])-1,kind:m[2]==='Level'?'level':'voice'};
  r.api=new LiveAPI(statecallback(r),'id '+all[j]);parameterRefs.push(r);
  r.api.property='value';acceptstate(r,r.api.get('value'));
 }
}
function syncstate(){for(var i=0;i<parameterRefs.length;i++)acceptstate(parameterRefs[i],parameterRefs[i].api.get('value'));}
function discover() {
 var candidates=[], seen={};
 function remember(s,slot) {
  var id=Number(s.id);
  if(isFinite(id) && id!==0 && !seen[id]) {seen[id]=true;candidates.push({api:s,slot:slot});}
 }
 // Application's preference-slot list may omit the integrated Push surface.
 // Also resolve the documented root paths; their ordering is independent.
 try {
  var raw=appAPI.get('control_surfaces'),all=[];
  if(!Array.isArray(raw))raw=[raw];
  for(var q=0;q<raw.length;q++)if(raw[q]==='id')all.push(Number(raw[++q]));
  if(!all.length)all=raw.filter(function(v){return isFinite(Number(v));}).map(Number);
  for(var i=0;i<all.length;i++)if(all[i])remember(api(all[i]),i);
 } catch(e) {}
 for(var k=0;k<16;k++) {
  try {remember(new LiveAPI(null,'control_surfaces '+k),-1);} catch(e) {}
 }
 discoveredCount=candidates.length;
 for(var i=0;i<candidates.length;i++) {
  var s=candidates[i].api;
  var names;
  try { names=s.call('get_control_names'); } catch(e) {continue;}
  if(!(Array.isArray(names))) names=[names];
  var pads=[];
  for(var j=0;j<names.length;j++) {
   var name=String(names[j]), match=/^(\d+)_Clip_(\d+)_Button$/.exec(name);
   if(match && Number(match[1])<8 && Number(match[2])<8) pads.push({name:name,x:Number(match[1]),y:Number(match[2])});
  }
  // Fail closed instead of guessing names/coordinates on another controller.
  if(pads.length!==64) continue;
  surface=s; surfaceSlot=candidates[i].slot; controls=pads;
  hasShift=names.indexOf('Shift_Button')!==-1;
  return true;
 }
 return false;
}
function acquire() {
 try {
  syncstate();
  for(var i=0;i<controls.length;i++) {
   var c=controls[i];
   if(c.y===7)continue; // Native note row retains pitch/pressure/slide MIDI.
   c.id=idOf(surface.call('get_control',c.name));
   if(!c.id) throw new Error('Missing pad '+c.name);
   surface.call('grab_control',c.name); grabbed.push(c);
   c.pressed=false; c.color=-1;
   c.api=new LiveAPI(c.y===0?null:callback(c),'id '+c.id);
   if(c.y!==0)c.api.property='value'; // Observe AFTER grabbing (required by Push 3).
  }
  active=true; bindshift(); redrawTicks=0; redraw(); status('Pads ready — use display banks');
 } catch(e) { release(); surface=null; status('Pad setup failed: '+e.message); }
}
function bindshift(){
 // Observe only. Never grab Shift or the encoders: their native functions remain.
 if(!hasShift)return;
 try{
  var id=idOf(surface.call('get_control','Shift_Button'));
  if(!id)return;
  var binding={api:null};shiftBinding=binding;
  binding.api=new LiveAPI(function(a){
   if(!active||shiftBinding!==binding||!a||a[0]!=='value')return;
   var down=Number(a[1])>0;
   schedule(function(){if(active&&shiftBinding===binding)outlet(1,'shift',down?1:0);});
  },'id '+id);
  binding.api.property='value';
 }catch(e){unbindshift();post('LIRA note tuning: Shift observation unavailable\n');}
}
function unbindshift(){
 var old=shiftBinding;shiftBinding=null;
 if(old)try{old.api.property='';}catch(e){}
 outlet(1,'shift',0);
}
function callback(c) {
 return function(a) {
  if(!active || c.y===0 || !a || a[0]!=='value') return;
  var down=Number(a[1])>0;
  if(down===c.pressed) return; // pressure/repeated values must not re-toggle
  c.pressed=down;
  if(!down)return;
  schedule(function(){
   if(!active)return;
   if(c.y===6) outlet(0,'voiceon'+(c.x+1),1-voices[c.x]);
   else if(c.y===0) return; // Disabled until native bank switching is verified.
   else if(c.y>=1 && c.y<=5) outlet(0,'level'+(c.x+1),Math.round((5-c.y)*127/4));
  });
 };
}
function redraw() {
 if(!active)return;
 for(var i=0;i<controls.length;i++)controls[i].color=-1;
 paint();
}
function paint() {
 if(!active)return;
 for(var i=0;i<controls.length;i++) {
  var c=controls[i], color=0;
  if(c.y===7)continue;
  if(c.y===6) color=voices[c.x]?PAIRS[Math.floor(c.x/2)]:0;
  if(c.y===0) color=0; // Disabled page row: native display banks remain available.
  // Five discrete fader positions: mute, 25%, 50%, 75%, 100% amplitude.
  if(c.y>=1 && c.y<=5 && levels[c.x]>0 && 5-c.y<=Math.round(levels[c.x]*4/127)) color=PAIRS[Math.floor(c.x/2)];
  if(color!==c.color) { c.api.call('send_value',color,1); c.color=color; }
 }
 status('Pads ready — use display banks');
}
function release() {
 unbindshift();
 if(active)outlet(0,'expressreset',0);
 active=false;
 for(var i=grabbed.length-1;i>=0;i--) {
  var c=grabbed[i];
  try { if(c.api) c.api.property=''; } catch(e) {}
  try { if(surface) surface.call('release_control',c.name); } catch(e) {}
  c.api=null; c.pressed=false; c.color=-1;
 }
 grabbed=[];
}
function tick() {
 if(!ready)return;
 try {
  if(!enabled) { release();status('Pads off');return; }
  var alive=self.get('is_active');
  trackView.goto('live_set view selected_track view');
  var selected=idOf(trackView.get('selected_device'));
  if(!Number(Array.isArray(alive)?alive[0]:alive) || selected!==Number(self.id)) {
   if(active)release(); status('Select LIRA Pads to play'); return;
  }
  if(!surface || !surface.id) {
   if(active)release();
   if((ticks++%4)!==0)return;
   if(!discover()) {status(discoveredCount?'No pad matrix found':'Waiting for Push');return;}
  }
  var layout=String(surface.get('pad_layout'));
  if(layout.indexOf('note.')!==0) {if(active)release();status('Press Note for LIRA pads');return;}
  if(!active)acquire();
  else if(++redrawTicks%4===0)redraw(); // Recover LEDs overwritten by Push layout redraws.
 } catch(e) {release();surface=null;status('Reconnecting to Push');}
}
function shutdown() { clock.cancel();work.cancel();queue=[];release();ready=false;surface=null;surfaceSlot=-1;controls=[];for(var i=0;i<parameterRefs.length;i++)try{parameterRefs[i].api.property='';}catch(e){}parameterRefs=[]; }
function notifydeleted() { shutdown(); }
