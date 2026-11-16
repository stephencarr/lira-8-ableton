const fs=require('fs'),vm=require('vm'),assert=require('assert');
let values={};
const c={outlet(port,name,value){values[name]=value;}};
vm.createContext(c);vm.runInContext(fs.readFileSync('src/expression.js','utf8'),c);
c.mpevoice(1);c.note(36,100);assert.equal(values.gate1,1);
c.bend(1/48);assert.equal(values.bend1,0);c.pressure(127);assert.equal(values.press1,1);assert.equal(values.bend1,2);
c.mpevoice(2);c.note(37,100);c.bend(-1/48);assert.equal(values.bend2,0);assert.equal(values.bend1,2);
c.mpevoice(1);c.note(36,0);assert.equal(values.gate1,0);assert.equal(values.bend1,0);assert.equal(values.press1,0);assert.equal(values.gate2,1);
// Duplicate pitches retain the remaining touch, and its expression, on release.
c.mpevoice(3);c.note(37,100);c.pressure(64);assert.equal(values.press2,64/127);
c.note(37,0);assert.equal(values.gate2,1);assert.equal(values.bend2,0);
c.mpevoice(2);c.note(37,0);assert.equal(values.gate2,0);
// Out-of-range notes cannot accidentally trigger another LIRA voice.
c.mpevoice(4);c.note(60,100);assert(Object.entries(values).filter(([k])=>k.startsWith('gate')).every(([,v])=>v===0));
// Plain MIDI chords and poly pressure still work, even without MPE voice IDs.
c.mpevoice(-1);c.note(38,100);c.note(39,100);c.polypressure(127,38);assert.equal(values.press3,1);assert.equal(values.gate4,1);
c.note(38,0);assert.equal(values.gate3,0);assert.equal(values.gate4,1);
c.reset();for(let i=1;i<=8;i++){assert.equal(values['gate'+i],0);assert.equal(values['bend'+i],0);assert.equal(values['press'+i],0);}
console.log('PASS: independent pressure expression, release resets, overlapping touches, note filtering, plain MIDI chords, poly pressure and panic reset.');

for(let i=0;i<8;i++){c.mpevoice(i+1);c.note(36+i,100);c.pressure(127);assert.equal(values['gate'+(i+1)],1);assert.equal(values['bend'+(i+1)],2);assert.equal(values['press'+(i+1)],1);c.note(36+i,0);assert.equal(values['gate'+(i+1)],0);}
console.log('PASS: all eight notes including voices 6–8, pressure couples pitch and sharpness, horizontal bend ignored.');
