"""Create a silent Live instrument that records a real Gen feedback comparison.

Run from the repo root; load build/LIRA-Feedback-Test.amxd in desktop Live.
It writes build/feedback-test.wav (four channels) and stops automatically.
No audio is sent to speakers. Only this harness removes stochastic delay noise.
"""
import copy,json,pathlib,re,struct
root=pathlib.Path(__file__).resolve().parents[1]
p=json.loads((root/'dist/LIRA-Push-Pads.maxpat').read_text())['patcher']
engine=next(e['box'] for e in p['boxes'] if e['box']['id']=='engine')
boxes=[];lines=[]
def add(i,text,cls='newobj',**kw):
    b=dict(id=i,maxclass=cls,text=text,patching_rect=[20,20+len(boxes)*24,300,22],**kw);boxes.append({'box':b});return b
def wire(a,b,o=0,n=0):lines.append({'patchline':dict(source=[a,o],destination=[b,n])})
add('tone','cycle~ 137');add('level','*~ 0.15');wire('tone','level')
for index,(gain,ready,totalfb,mod) in enumerate([(0,1,1,80),(127,0,1,80),(127,1,1,80),(127,1,0,0)]):
    e=copy.deepcopy(engine);e['id']='e'+str(index);boxes.append({'box':e})
    c=e['patcher']['boxes'][0]['box']['code']
    for n,v in dict(extgain=gain,extready=ready,totalfb=totalfb,mod1=mod,voiceon1=1,source1=2).items():
        c=re.sub(r'(Param '+n+r'\()[^,]+',r'\g<1>'+str(v),c)
    c=c.replace('n=noise()*0.001;','n=0;')
    # Record the oscillator itself, upstream of the external-audio summing point.
    c=c.replace('out1=master*lira_ramp(pow(volume/127,2),23.22);','out1=v1*0.1;')
    e['patcher']['boxes'][0]['box']['code']=c
    wire('level',e['id']);wire('level',e['id'],0,1);wire(e['id'],'record',0,index)
add('record','sfrecord~ 4');add('boot','live.thisdevice');add('defer','deferlow');wire('boot','defer')
add('start','t b b');wire('defer','start')
add('open','open '+str(root/'build/feedback-test.wav'),'message');wire('start','open',1);wire('open','record')
add('settle','delay 1000');wire('start','settle');add('one','1','message');wire('settle','one');wire('one','record')
add('end','delay 4000');wire('settle','end');add('zero','0','message');wire('end','zero');wire('zero','record')
add('silence','sig~ 0');add('out','plugout~');wire('silence','out');wire('silence','out',0,1)
p.update(boxes=boxes,lines=lines,parameters={},openinpresentation=0,dependency_cache=[])
r=json.dumps({'patcher':p}).encode()+b'\0'
(root/'build/LIRA-Feedback-Test.amxd').write_bytes(b'ampf'+struct.pack('<I',4)+b'iiii'+b'meta'+struct.pack('<II',4,0)+b'ptch'+struct.pack('<I',len(r))+r)
print('Load build/LIRA-Feedback-Test.amxd in Live; allow six seconds for capture.')
