const fs=require('fs'),vm=require('vm'),assert=require('assert');
const sign=Number(process.env.LIRA_ID_SIGN)||1;
let pending=[],selected=5,tap=1,active=1,channelsAvailable=true,trackCount=2,sets=[];
let types=[{display_name:'Ext. In',identifier:17},{display_name:'Bass',identifier:31},{display_name:'Mic',identifier:52},{display_name:'No Input',identifier:99}];
let type=types[3],channel={display_name:'',identifier:0};
function channels(){return !channelsAvailable?[]:type.identifier===17?['1','2','1 / 2'].map((n,i)=>({display_name:n,identifier:100+i})):['Pre FX','Post FX','Post Mixer'].map((n,i)=>({display_name:n,identifier:200+i}));}
class Task{constructor(fn,ctx){this.fn=fn.bind(ctx);}schedule(){if(!pending.includes(this))pending.push(this);}cancel(){pending=pending.filter(x=>x!==this);}repeat(){}}
class LiveAPI{
 constructor(cb,path){this.path=path;this.id=path==='this_device'?sign:path==='live_set'?2*sign:Number(path.split(' ')[1]);}
 get(k){
  if(k==='parameters')return ['id',10*sign,'id',11*sign];
  if(k==='name')return [this.id===10*sign?'Audio From':this.id===11*sign?'Audio Tap':this.id===30*sign?'Bass':'Mic'];
  if(k==='value')return [this.id===10*sign?selected:tap];
  if(k==='is_active')return [active];
  if(k==='audio_inputs')return ['id',20*sign];
  if(k==='tracks')return ['id',30*sign,'id',31*sign].slice(0,trackCount*2);
  if(k==='has_audio_output')return [1];
  const obj={available_routing_types:types,available_routing_channels:channels(),routing_type:type,routing_channel:channel};
  if(k in obj)return [JSON.stringify({[k]:obj[k]})];
  throw Error(k);
 }
 set(k,v){sets.push(k);if(k==='routing_type'){type=JSON.parse(v);channel={display_name:'',identifier:0};}else if(k==='routing_channel')channel=JSON.parse(v);else throw Error(k);}
}
let gate,status;
const ctx={LiveAPI,Task,outlet(port,a,b){if(port===0){assert.equal(a,'extready');gate=b;}else status=b;}};
vm.createContext(ctx);vm.runInContext(fs.readFileSync('src/audio-input.js','utf8'),ctx);
function drain(){let n=30;while(pending.length&&n--)pending.shift().fn();assert(n>0,'routing task must settle');}
ctx.init();drain();assert.equal(type.identifier,52);assert.equal(channel.display_name,'Post FX');assert.equal(gate,1);
assert(status.includes('Mic'),'show actual source name');
sets=[];for(let i=0;i<10;i++)ctx.apply();assert.equal(sets.length,0,'unchanged routes must not write repeatedly');
ctx.tap(2);drain();assert.equal(channel.display_name,'Post Mixer');
for(let i=1;i<=3;i++){ctx.source(i);drain();assert.equal(type.identifier,17);assert.equal(channel.display_name,['1','2','1 / 2'][i-1]);assert.equal(gate,1);}
ctx.source(0);drain();assert.equal(gate,0);assert.equal(type.identifier,99);
ctx.source(67);drain();assert.equal(gate,0);assert(status.includes('unavailable'));
ctx.source(4);drain();assert.equal(type.identifier,31);assert.equal(gate,1);
active=0;ctx.apply();assert.equal(gate,0);active=1;ctx.apply();assert.equal(gate,1);
channelsAvailable=false;ctx.apply();assert.equal(gate,0);channelsAvailable=true;ctx.apply();assert.equal(gate,1);
// Reordering tracks is explicit positional selection; a missing position mutes input.
ctx.source(5);drain();trackCount=1;ctx.apply();assert.equal(gate,0);assert.equal(type.identifier,99);
trackCount=2;ctx.apply();drain();assert.equal(type.identifier,52);assert.equal(gate,1);
ctx.shutdown();assert.equal(gate,0);assert.equal(pending.length,0);
console.log('PASS: recalled source/tap, native I/O IDs, mono/stereo inputs, track taps, missing inputs, no repeated routing writes and shutdown.');
