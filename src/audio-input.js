// Native audio input for the LIRA instrument. All API work runs in a Task.
// Fixed parameter enums: Off, Input 1, Input 2, Input 1/2, Track 1..64.
// Track choices mean current track positions. No control-surface API is used.
autowatch=0; inlets=1; outlets=2;
var device=null, bus=null, clock=null, work=null, started=false;
var selected=0, tapIndex=1, ready=-1, lastStatus='';
function ids(a){var r=[];for(var i=0;i<a.length;i++)if(a[i]==='id'&&Number(a[i+1]))r.push(Number(a[++i]));return r;}
function value(a){return Number(Array.isArray(a)?a[0]:a)||0;}
function data(api,key){var a=api.get(key);var d=JSON.parse(Array.isArray(a)?a.join(' '):a);return d[key];}
function status(s){if(s!==lastStatus){lastStatus=s;outlet(1,'set',s);}}
function gate(v){if(v!==ready){ready=v;outlet(0,'extready',v);}}
function schedule(ms){if(!started)return;if(!work)work=new Task(apply,this);work.cancel();work.schedule(ms||0);}
function source(v){selected=Math.max(0,Math.min(67,Math.round(Number(v)||0)));schedule();}
function tap(v){tapIndex=Math.max(0,Math.min(2,Math.round(Number(v)||0)));schedule();}
function init(){
 shutdown();started=true;gate(0);
 try {
  device=new LiveAPI(null,'this_device');
  // Read recalled parameter values; do not overwrite a saved Live Set with defaults.
  var ps=ids(device.get('parameters'));
  for(var i=0;i<ps.length;i++){
   var p=new LiveAPI(null,'id '+ps[i]);var n=p.get('name').join(' ');
   if(n==='Audio From')selected=value(p.get('value'));
   if(n==='Audio Tap')tapIndex=value(p.get('value'));
  }
  clock=new Task(apply,this);clock.interval=1000;clock.repeat();schedule();
 }catch(e){status('Audio input unavailable: '+String(e));}
}
function chooseType(types,name){
 var found=types.filter(function(t){return t.display_name===name;});
 return found.length===1?found[0]:null;
}
function none(types){
 var off=chooseType(types,'No Input');
 if(off&&data(bus,'routing_type').identifier!==off.identifier)bus.set('routing_type',JSON.stringify(off));
}
function apply(){
 if(!started||!device)return;
 try {
  if(!value(device.get('is_active'))){gate(0);return;}
  var ports=ids(device.get('audio_inputs'));
  if(!ports.length){gate(0);status('No audio input bus');return;}
  if(!bus||Number(bus.id)!==ports[0])bus=new LiveAPI(null,'id '+ports[0]);
  var types=data(bus,'available_routing_types');
  if(selected===0){gate(0);none(types);status('Audio input off');return;}
  var wanted=null, chan='', description='';
  if(selected<=3){
   wanted=chooseType(types,'Ext. In');chan=['1','2','1/2'][selected-1];description='Input '+chan;
  }else{
   var index=selected-4;
   var tracks=ids(new LiveAPI(null,'live_set').get('tracks'));
   if(index>=tracks.length){gate(0);none(types);status('Track '+(index+1)+' is unavailable');return;}
   var track=new LiveAPI(null,'id '+tracks[index]);
   var name=track.get('name').join(' ');
   if(!value(track.get('has_audio_output'))){gate(0);none(types);status('Track '+(index+1)+' has no audio');return;}
   wanted=chooseType(types,name)||chooseType(types,(index+1)+'-'+name);
   chan=['Pre FX','Post FX','Post Mixer'][tapIndex];description='Track '+(index+1)+': '+name+' / '+chan;
  }
  if(!wanted){gate(0);none(types);status('Audio source unavailable or ambiguous');return;}
  if(data(bus,'routing_type').identifier!==wanted.identifier){
   gate(0);bus.set('routing_type',JSON.stringify(wanted));schedule(30);return;
  }
  var channels=data(bus,'available_routing_channels');
  var match=channels.filter(function(c){return String(c.display_name).replace(/\s/g,'')===chan.replace(/\s/g,'');})[0];
  if(!match){gate(0);status(description+' unavailable');return;}
  if(data(bus,'routing_channel').identifier!==match.identifier){
   gate(0);bus.set('routing_channel',JSON.stringify(match));schedule(30);return;
  }
  gate(1);status(description+' · raise Audio In');
 }catch(e){gate(0);status('Audio routing error: '+String(e));}
}
function shutdown(){
 started=false;if(clock)clock.cancel();if(work)work.cancel();clock=null;work=null;
 gate(0);bus=null;device=null;
}
