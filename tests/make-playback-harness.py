"""Test all eight latches and MIDI notes through the complete production patch.

Load build/LIRA-Playback-Test.amxd on a temporary MIDI track in desktop Live.
It records internally for 18 seconds, sends silence to the speakers and stops.
Unlike a Gen-only test, it retains live.text -> DSP and mpeparse -> expression.
"""
import json,pathlib,struct
root=pathlib.Path(__file__).resolve().parents[1]
p=json.loads((root/'dist/LIRA-Push-Pads.maxpat').read_text())['patcher']
by={e['box']['id']:e['box'] for e in p['boxes']}
initial=dict(padmode=0,volume=64,dmix=0,distmix=0,feedback=0,vibrato=0,totalfb=0)
initial.update({f'mod{i}':0 for i in range(1,5)})
initial.update({f'fast{i}':1 for i in range(1,5)})
for n,v in initial.items():by[n]['saved_attribute_attributes']['valueof']['parameter_initial']=[v]
p['lines']=[e for e in p['lines'] if e['patchline']['destination'][0]!='output']
def add(i,text=None,cls='newobj',**kw):
    b=dict(id=i,maxclass=cls,patching_rect=[20,1400,300,22],**kw)
    if text is not None:b['text']=text
    p['boxes'].append({'box':b})
def wire(a,b,o=0,i=0):p['lines'].append({'patchline':dict(source=[a,o],destination=[b,i])})
add('testsilence','sig~ 0');wire('testsilence','output');wire('testsilence','output',0,1)
add('testrecord','sfrecord~ 2');wire('engine','testrecord');wire('engine','testrecord',1,1)
add('testboot','live.thisdevice');add('testdefer','deferlow');wire('testboot','testdefer')
add('testopen','open '+str(root/'build/playback-capture.wav'),'message');wire('testdefer','testopen');wire('testopen','testrecord')
add('testmidi','iter');wire('testmidi','expressparse')
def at(ms,msg,target):
    i='testevent'+str(len(p['boxes']))
    add(i,'delay '+str(ms));wire('testdefer',i)
    add(i+'msg',msg,'message');wire(i,i+'msg');wire(i+'msg',target)
at(1500,'1','testrecord')
for i in range(8):
    at(2000+i*1000,'1','voiceon'+str(i+1));at(2600+i*1000,'0','voiceon'+str(i+1))
    at(10000+i*1000,f'144 {36+i} 100','testmidi');at(10600+i*1000,f'128 {36+i} 0','testmidi')
at(19500,'0','testrecord')
raw=json.dumps({'patcher':p},indent=2).encode()+b'\0'
(root/'build/LIRA-Playback-Test.amxd').write_bytes(b'ampf'+struct.pack('<I',4)+b'iiii'+b'meta'+struct.pack('<II',4,0)+b'ptch'+struct.pack('<I',len(raw))+raw)
print('Built complete-patch playback test; load in Live and allow 21 seconds.')
