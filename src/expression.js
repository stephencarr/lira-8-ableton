// Native MPE from midiin -> mpeparse. Expression never changes saved tuning.
inlets=1;outlets=1;
var zone=0, first=0, voice=-1, notes={}, serial=0;
function zoneindex(v){zone=Number(v);}
function zonefirst(v){first=Number(v);}
function mpevoice(v){voice=Number(v);}
function key(){return first+':'+zone+':'+voice;}
function record(){var k=key();if(!notes[k])notes[k]={target:-1,pitch:-1,bend:0,pressure:0,order:0};return notes[k];}
function emit(i){
 var chosen=null;
 for(var k in notes){var n=notes[k];if(n.target===i&&(!chosen||n.order>chosen.order))chosen=n;}
 outlet(0,'gate'+(i+1),chosen?1:0);
 outlet(0,'bend'+(i+1),chosen?chosen.bend:0);
 outlet(0,'press'+(i+1),chosen?chosen.pressure:0);
}
function note(p,v){
 p=Number(p);v=Number(v);
 // Unvoiced conventional MIDI uses pitch as identity, allowing chords.
 var n=voice<0?(notes['plain:'+p]||(notes['plain:'+p]={target:-1,pitch:p,bend:0,pressure:0,order:0})):record();
 var old=n.target;
 if(v>0){n.pitch=p;n.target=p>=36&&p<=43?p-36:-1;n.order=++serial;}
 else if(n.pitch===p){n.target=-1;n.bend=0;n.pressure=0;}
 if(old>=0)emit(old);
 if(n.target>=0)emit(n.target);
}
function bend(v){} // Horizontal movement no longer affects tuning.
function applypressure(n,v){n.pressure=Math.max(0,Math.min(127,Number(v)||0))/127;n.bend=n.pressure*2;}
function pressure(v){if(voice<0)return;var n=record();applypressure(n,v);if(n.target>=0)emit(n.target);}
function polypressure(v,p){for(var k in notes){var n=notes[k];if(n.target>=0&&n.pitch===Number(p)){applypressure(n,v);emit(n.target);}}}
function reset(){notes={};for(var i=0;i<8;i++)emit(i);}
function notifydeleted(){reset();}
