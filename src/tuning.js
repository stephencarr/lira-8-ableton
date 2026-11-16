// Temporary chromatic tuning. Keeps saved 0..127 parameters and all banks fixed.
// No synthesis changes: invert the existing per-voice tuning law, including Pitch.
inlets=1; outlets=5;
var ranges=[[-16,93],[-16,93],[7,109],[9,107],[20,116.54],[20,116.54],[33,126.24],[33,131.22]];
var values={tune1:64,tune2:68,tune3:55,tune4:60,tune5:45,tune6:50,tune7:38,tune8:43,pitch1:63,pitch2:63};
var names=Object.keys(values), refs={}, formats={}, running=false, held=false, desktop=false, snapping=false;
var origin=[63,63], steps=[0,0];
var suspended=false, resumeTask=new Task(resume,this);
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function offset(v){return 12*Math.log(0.01+1.99*v/127)/Math.LN2;}
function midi(i,v,p){return ranges[i][0]+v/127*(ranges[i][1]-ranges[i][0])+offset(p);}
function raw(i,n,p){return 127*(n-ranges[i][0]-offset(p))/(ranges[i][1]-ranges[i][0]);}
function note(n){n=Math.round(n);return ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][((n%12)+12)%12]+(Math.floor(n/12)-2);}
function output(n,v){values[n]=v;outlet(0,n,v);outlet(3,n,'set',v);}
function write(n,v){output(n,v);outlet(1,n,'set',v);}
function format(n,f,label){
 if(formats[n]!==f){formats[n]=f;outlet(1,n,'_parameter_units',f);}
 outlet(2,n,'set',label);
}
function refresh(){
 for(var i=0;i<8;i++){
  var n='tune'+(i+1),m=midi(i,values[n],values[i<4?'pitch1':'pitch2']);
  var label=note(m)+(Math.abs(m-Math.round(m))>0.001?'~':'');
  format(n,snapping?label+' %.2f':'%.0f','Tune '+(i+1)+(snapping?' · '+label:''));
 }
 for(var g=0;g<2;g++){
  var label=(steps[g]>=0?'+':'')+steps[g]+'st';
  format('pitch'+(g+1),snapping?label+' %.1f':'%.0f','Pitch '+(g===0?'1234':'5678')+(snapping?' · '+label:''));
 }
}
function mode(){
 var next=running&&!suspended&&(held||desktop);
 if(next===snapping)return;
 snapping=next;
 if(next){origin=[values.pitch1,values.pitch2];steps=[0,0];}
 refresh();
 outlet(4,'set',next?'NOTE TUNE · turn Tune for notes / Pitch for semitone transposition':'Hold Push Shift while turning Tune to choose notes. Release for continuous tuning.');
}
function shift(v){held=Number(v)>0;mode();}
function manual(v){desktop=Number(v)>0;mode();}
function preset(){suspended=true;mode();resumeTask.cancel();resumeTask.schedule(50);}
function resume(){suspended=false;mode();}
function automated(n){try{return refs[n]&&Number(refs[n].get('automation_state')[0])===1;}catch(e){return true;}}
function input(n,v){
 if(!Object.prototype.hasOwnProperty.call(values,n))return;
 v=Number(v);if(!isFinite(v))return;v=clamp(v,0,127);
 var old=values[n],delta=v-old;
 // 'set' writes do not emit from live.dial. Also ignore float round-off echoes.
 if(Math.abs(delta)<0.00002){output(n,old);return;}
 if(!snapping||automated(n)){
  output(n,v);
  if(snapping){if(n.indexOf('pitch')===0){var g=Number(n.slice(5))-1;origin[g]=v;steps[g]=0;}refresh();}
  return;
 }
 var direction=delta>0?1:-1,result;
 if(n.indexOf('tune')===0){
  var i=Number(n.slice(4))-1,p=values[i<4?'pitch1':'pitch2'];
  var current=midi(i,old,p);
  var target=direction>0?Math.floor(current+0.0001)+1:Math.ceil(current-0.0001)-1;
  target=clamp(target,Math.ceil(midi(i,0,p)-0.00001),Math.floor(midi(i,127,p)+0.00001));
  result=clamp(raw(i,target,p),0,127);
 }else{
  var g=Number(n.slice(5))-1,next=steps[g]+direction;
  result=127*((0.01+1.99*origin[g]/127)*Math.pow(2,next/12)-0.01)/1.99;
  if(result<0||result>127){write(n,old);return;}
  steps[g]=next;
 }
 write(n,result);refresh();
}
function anything(){if(arguments.length)input(messagename,arguments[0]);}
function init(){
 resumeTask.cancel();suspended=false;running=false;held=false;desktop=false;snapping=false;refs={};formats={};
 try{
  var device=new LiveAPI(null,'this_device'),ps=device.get('parameters');
  for(var i=0;i<ps.length;i++)if(ps[i]==='id'){
   var p=new LiveAPI(null,'id '+Number(ps[++i])),name=String(p.get('name'));
   var match=/^(Tune [1-8]|Pitch (?:1234|5678|1[–-]4|5[–-]8))$/.exec(name);
   if(!match)continue;
   var n=name.indexOf('Tune')===0?'tune'+name.slice(5):/^Pitch 1/.test(name)?'pitch1':'pitch2';
   refs[n]=p;output(n,Number(p.get('value')[0]));
  }
  if(Object.keys(refs).length!==10)throw new Error('Missing tuning parameters');
  running=true;refresh();
  outlet(4,'set','Hold Push Shift while turning Tune to choose notes. Release for continuous tuning.');
 }catch(e){shutdown();outlet(4,'set','Note tuning unavailable: '+String(e));}
}
function shutdown(){resumeTask.cancel();suspended=false;held=false;desktop=false;running=false;mode();refs={};}
function notifydeleted(){shutdown();}
