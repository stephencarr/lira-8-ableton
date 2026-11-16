const fs=require('fs'),vm=require('vm'),assert=require('assert');
const sign=Number(process.env.LIRA_ID_SIGN)||1;
const names=Array.from({length:8},(_,i)=>'tune'+(i+1)).concat(['pitch1','pitch2']);
const saved=[74.626067,68,55,60,45,50,38,43,63,63],automation=Array(10).fill(0);
let events=[];
class LiveAPI{
 constructor(cb,path){this.id=path==='this_device'?999:Math.abs(Number(path.split(' ')[1]));}
 get(k){if(k==='parameters')return names.flatMap((_,i)=>['id',(i+1)*sign]);
  const i=this.id-1;
  if(k==='name')return [i<8?'Tune '+(i+1):i===8?'Pitch 1234':'Pitch 5678'];
  if(k==='value')return [saved[i]];
  if(k==='automation_state')return [automation[i]];
  throw Error(k);
 }
}
class Task{constructor(fn,ctx){this.fn=fn.bind(ctx);}cancel(){}schedule(){}}
const ctx={LiveAPI,Task,outlet(...a){events.push(a);}};
vm.createContext(ctx);vm.runInContext(fs.readFileSync('src/tuning.js','utf8'),ctx);
const close=(a,b,eps=1e-7)=>assert(Math.abs(a-b)<eps,`${a} != ${b}`);
ctx.init();assert.equal(ctx.values.tune1,saved[0]);assert(!ctx.snapping);
events=[];ctx.shift(1);assert(ctx.snapping);
assert(!events.some(e=>e[0]===0||e[0]===3||e[2]==='set'&&e[0]===1),'pressing Shift must not retune');
const before=ctx.values.tune1;
ctx.input('tune1',before+0.001);close(ctx.midi(0,ctx.values.tune1,63),49);
assert(ctx.formats.tune1.startsWith('C#2 '));
ctx.input('tune1',ctx.values.tune1-0.001);close(ctx.midi(0,ctx.values.tune1,63),48);
assert(ctx.formats.tune1.startsWith('C2 '));
const exact=ctx.values.tune1;ctx.shift(0);close(ctx.values.tune1,exact);
assert.equal(ctx.formats.tune1,'%.0f');ctx.input('tune1',exact+0.123);close(ctx.values.tune1,exact+0.123);
// Invert every voice's nonuniform range, including extreme shared Pitch settings.
for(let i=0;i<8;i++)for(const p of [0,1,30,63,100,127]){
 const lo=Math.ceil(ctx.midi(i,0,p)),hi=Math.floor(ctx.midi(i,127,p));
 for(let n=lo;n<=hi;n++){const v=ctx.raw(i,n,p);assert(v>=-1e-8&&v<=127+1e-8);close(ctx.midi(i,v,p),n);}
}
assert.equal(ctx.note(36),'C1');assert.equal(ctx.note(60),'C3');assert.equal(ctx.note(-1),'B-3');
ctx.shift(1);
const chord=Array.from({length:4},(_,i)=>ctx.midi(i,ctx.values['tune'+(i+1)],ctx.values.pitch1));
ctx.input('pitch1',ctx.values.pitch1+0.01);
for(let i=0;i<4;i++)close(ctx.midi(i,ctx.values['tune'+(i+1)],ctx.values.pitch1),chord[i]+1);
ctx.input('pitch1',ctx.values.pitch1-0.01);close(ctx.values.pitch1,63);
// Exact semitone stepping and valid endpoints on all eight voices.
for(let i=0;i<8;i++){
 const n='tune'+(i+1),p=ctx.values[i<4?'pitch1':'pitch2'];
 for(const v of [0,127,52.31]){ctx.values[n]=v;ctx.input(n,v===127?v-0.001:v+0.001);
  const pitch=ctx.midi(i,ctx.values[n],p);close(pitch,Math.round(pitch));assert(ctx.values[n]>=0&&ctx.values[n]<=127);
 }
}
automation[1]=1;ctx.input('tune2',22.25);close(ctx.values.tune2,22.25);automation[1]=0;
const old=ctx.values.tune1;ctx.input('tune1',NaN);close(ctx.values.tune1,old);
ctx.manual(1);ctx.shift(0);assert(ctx.snapping,'desktop toggle remains independent');ctx.manual(0);assert(!ctx.snapping);
ctx.shift(1);ctx.preset();ctx.input('tune1',52.123);close(ctx.values.tune1,52.123);ctx.resume();assert(ctx.snapping);
ctx.shift(1);ctx.shutdown();assert(!ctx.snapping);assert.equal(ctx.formats.tune1,'%.0f');
console.log('PASS: recalled values, exact note inversion on eight voices, Shift/release without jumps, fractional writeback, shared transposition, automation bypass and lifecycle.');
