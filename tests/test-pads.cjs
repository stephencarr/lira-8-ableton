const fs=require('fs'),vm=require('vm'),assert=require('assert');
const code=fs.readFileSync(process.env.LIRA_TEST_CONTROLLER||'dist/LIRA-Pads-controller.js','utf8');
let pending=[], events=[], observers=new Map(), owned=new Set(), layout='note.melodic.64_notes', appointed=100, enabled=1, missing=false, rootOnly=false, failGrab=-1;
const idSign=Number(process.env.LIRA_ID_SIGN)||1;
const surfaceID=200*idSign;
const padID=i=>(300+i)*idSign;
const shiftID=400*idSign;
const hardwareLEDs=new Map();
const savedLevels=[0,32,64,95,127,64,32,127], savedVoices=Array(8).fill(0);
const padNames=Array.from({length:64},(_,i)=>`${i%8}_Clip_${Math.floor(i/8)}_Button`).concat(['Shift_Button']);
class Task {constructor(fn,ctx){this.fn=fn.bind(ctx);}schedule(){if(!pending.includes(this))pending.push(this);}repeat(){}cancel(){pending=pending.filter(x=>x!==this);}}
class LiveAPI {
 constructor(cb,path){this.cb=cb;this.path=path;this.id=path==='this_device'?100:path==='live_set'?101:path==='live_app'?102:Number(path.split(' ')[1]);if(path.startsWith('control_surfaces '))this.id=!missing&&rootOnly&&path==='control_surfaces 2'?surfaceID:0;this.type='ControlSurface';}
 goto(path){this.path=path;}
 get(name){if(name==='parameters')return Array.from({length:16},(_,i)=>['id',500+i]).flat();if(name==='name')return ['Voice '+((this.id-500)%8+1)+' '+(this.id<508?'Level':'On')];if(name==='value')return [this.id<508?savedLevels[this.id-500]:savedVoices[this.id-508]];if(name==='control_surfaces')return missing||rootOnly?[]:['id',0,'id',String(199*idSign),'id',0,'id',String(surfaceID)];if(name==='appointed_device'||name==='selected_device')return ['id',appointed];if(name==='is_active')return enabled;if(name==='pad_layout')return [layout];throw Error(name);}
 set property(p){this.prop=p;if(p==='value')observers.set(this.id,this.cb);else observers.delete(this.id);}
 call(name,...a){if(name==='send_value')hardwareLEDs.set(this.id,a[0]);assert(['get_control_names','get_control','grab_control','release_control','send_value'].includes(name),'Unexpected API call: '+name);events.push([name,...a]);if(name==='get_control_names')return this.id===surfaceID?padNames:['Unrelated_Button'];if(name==='get_control')return ['id',a[0]==='Shift_Button'?shiftID:padID(padNames.indexOf(a[0]))];if(name==='grab_control'){if(owned.size===failGrab)throw Error('simulated acquisition failure');owned.add(a[0]);}if(name==='release_control')owned.delete(a[0]);}
}
const ctx={Task,LiveAPI,post(){},outlet(n,...a){if(a.length===1&&Array.isArray(a[0]))a=a[0];events.push(['outlet',n,...a]);if(n===0){if(a[0]==='padpage')ctx.page(a[1]);else if(a[0].startsWith('voiceon')){let i=Number(a[0].slice(7))-1;savedVoices[i]=a[1];ctx.state(i,a[1]);}else if(a[0].startsWith('level')){let i=Number(a[0].slice(5))-1;savedLevels[i]=a[1];ctx.level(i,a[1]);}}}};vm.createContext(ctx);vm.runInContext(code,ctx);
function drain(){let guard=100;while(pending.length&&guard--)pending.shift().fn();assert(guard>0,'no feedback loop');}
function press(x,y,value){observers.get(padID(y*8+x))(['value',value]);drain();}
ctx.init();assert.equal(owned.size,56);assert.equal(ctx.active,true);assert.deepEqual(Array.from(ctx.levels),savedLevels,'first draw must match saved values, not defaults');assert.equal(ctx.controls.find(c=>c.x===0&&c.y===5).color,0);
// Simulate a late native layout redraw after a successful initial LED send.
const litPad=padID(4+8);assert(hardwareLEDs.get(litPad)>0);
hardwareLEDs.clear();for(let i=0;i<4;i++)ctx.tick();
assert(hardwareLEDs.get(litPad)>0,'periodic repaint restores lights even though cached colours are unchanged');
hardwareLEDs.clear();ctx.level(4,127);drain();
assert(hardwareLEDs.get(litPad)>0,'same-value parameter feedback forces a repaint without pressing mute');
press(0,6,127);assert.equal(ctx.voices[0],1);press(0,6,80);assert.equal(ctx.voices[0],1);press(0,6,0);assert.equal(ctx.voices[0],1);press(0,6,127);assert.equal(ctx.voices[0],0);press(0,6,0);
for(let x=0;x<8;x++){
 const before=ctx.pageIndex;
 assert(!observers.has(padID(x)),'disabled row must have no observer');
 ctx.callback(ctx.controls.find(c=>c.x===x&&c.y===0))(['value',127]);drain();
 assert.equal(ctx.pageIndex,before,'recovery top row must be inert');
 assert.equal(ctx.controls.find(c=>c.x===x&&c.y===0).color,0);
}
assert(!events.some(e=>e[0]==='store_chosen_bank'),'crash-associated API must never be called');
assert(!code.includes(".call('store_chosen_bank'"),'crash-associated API must be absent');
assert(!observers.has(padID(56)),'bottom row must retain native MPE');
for(let x=0;x<8;x++){
 for(let y=1;y<=5;y++){press(x,y,127);press(x,y,0);assert.equal(ctx.levels[x],Math.round((5-y)*127/4));}
 assert.equal(ctx.controls.find(c=>c.x===x&&c.y===5).color,0,'muted fader is dark');
}
assert.equal(ctx.controls.find(c=>c.x===0&&c.y===6).color,0,'unlatched voice is completely dark');
ctx.state(3,1);drain();assert.equal(ctx.controls.find(c=>c.x===3&&c.y===6).color,ctx.PAIRS[1]);
savedLevels[4]=32;observers.get(504)(['value',32]);drain();assert.equal(ctx.levels[4],32,'encoder/automation changes update LEDs');
layout='session';ctx.tick();assert.equal(owned.size,0);assert.equal(observers.size,16);
layout='note.melodic.64_notes';ctx.tick();assert.equal(owned.size,56);
appointed=999;ctx.tick();assert.equal(owned.size,0);appointed=100;ctx.tick();assert.equal(owned.size,56);
ctx.enable(0);drain();assert.equal(owned.size,0);ctx.enable(1);drain();assert.equal(owned.size,56);
enabled=0;ctx.tick();assert.equal(owned.size,0);enabled=1;ctx.tick();assert.equal(owned.size,56);
ctx.notifydeleted();assert.equal(owned.size,0);assert.equal(observers.size,0);assert.equal(pending.length,0);
failGrab=10;ctx.init();assert.equal(owned.size,0,'failed acquisition releases all partial grabs');assert.equal(observers.size,16);ctx.shutdown();failGrab=-1;
missing=true;ctx.init();assert.equal(owned.size,0);assert.match(ctx.lastStatus,/Waiting for Push/);missing=false;for(let i=0;i<4;i++)ctx.tick();assert.equal(owned.size,56,'late connection retried');ctx.shutdown();
console.log('PASS: all voice latches, release/pressure filtering, inert top row, LED sync, native MPE row exclusion and eight faders, Session/device/track/enable lifecycle, partial failure cleanup and reconnect. Mocked API; not a hardware test.');

rootOnly=true;ctx.init();assert.equal(owned.size,56,'root path finds integrated controller with empty application list');assert.equal(ctx.discoveredCount,1);ctx.shutdown();rootOnly=false;
console.log('PASS: empty application surface list with valid root-path surface; invalid earlier slots skipped.');

ctx.init();observers.get(shiftID)(['value',127]);drain();assert(events.some(e=>e[0]==='outlet'&&e[1]===1&&e[2]==='shift'&&e[3]===1));assert(!owned.has('Shift_Button'));const stale=observers.get(shiftID);ctx.release();stale(['value',127]);drain();assert.equal(events.filter(e=>e[0]==='outlet'&&e[1]===1&&e[2]==='shift').at(-1)[3],0);assert(!observers.has(shiftID));ctx.shutdown();
console.log('PASS: passive Shift observation, no Shift grab, release resets tuning and ignores stale notifications.');
