import json, struct, pathlib, shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'build/LIRA-Push'; OUT.mkdir(parents=True,exist_ok=True)
params=[]
def param(n,label,val=0,maximum=127): params.append((n,label,val,maximum))
for i,v in enumerate([64,68,55,60,45,50,38,43],1): param('tune'+str(i),'Tune '+str(i),v)
for name,label,values in [('sharp','Sharp',[40]*4),('mod','FM',[0]*4),('source','Source',[1]*4),('fast','Fast',[0]*4)]:
 for p,v in enumerate(values): param(name+str(p+1),label+' '+['12','34','56','78'][p],v,2 if name=='source' else 1 if name=='fast' else 127)
for n,l,v,m in [('pitch1','Pitch 1234',63,127),('pitch2','Pitch 5678',63,127),('hold1','Hold 1234',0,127),('hold2','Hold 5678',0,127),('lfo1','LFO A',64,127),('lfo2','LFO B',72,127),('link','LFO Link',0,1),('andor','LFO AND OR',0,1),('routing','FM Routing',0,1),('totalfb','Total FB',0,1),('vibrato','Vibrato',0,1),('quantize','Quantize',0,1),('time1','Delay Time 1',60,127),('time2','Delay Time 2',68,127),('dmod1','Delay Mod 1',0,127),('dmod2','Delay Mod 2',0,127),('feedback','Feedback',35,127),('dmix','Delay Mix',30,127),('dsource','Delay Source',1,2),('dwave','Delay Wave',0,1),('drive','Drive',20,127),('distmix','Dist Mix',30,127),('volume','Master',80,127)]:param(n,l,v,m)
for i in range(1,9): param('voiceon'+str(i),'Voice '+str(i)+' On',0,1)
param('extgain','Audio In',0)
param('extsource','Audio From',0,67)
param('exttap','Audio Tap',1,2)
code=r'''
// Adapted from LIRA-8, Copyright Miguel Moreno. See License.txt.
// Gen port: explicit 64-sample inter-pair feedback; see port notes.
lira_sat(x) { z=clamp(x,-3,3); return z*(27+z*z)/(27+9*z*z); }
lira_ramp(x,ms) {
 History previous(0);
 History value(0);
 History remaining(0);
 History increment(0);
 if (x != previous) {
   remaining = max(1, ms * samplerate / 1000);
   increment = (x - value) / remaining;
 }
 previous = x;
 if (remaining > 0) {
   value = value + increment;
   remaining = max(0, remaining - 1);
 } else {
   value = x;
 }
 return value;
}

lira_lp(x,f) { History y(0); a=clamp(6.28318530718*f/samplerate,0,1); y=y+a*(x-y); return y; }
lira_hp(x,f) {
 History input_memory(0);
 History output_memory(0);
 coefficient = clamp(1 - 6.28318530718 * f / samplerate, 0, 1);
 result = (1 + coefficient) * 0.5 * (x - input_memory) + coefficient * output_memory;
 input_memory = x;
 output_memory = result;
 return result;
}

lira_blep(p,d) { a=p/max(d,0.00000001); b=(p-1)/max(d,0.00000001); return p<d ? 2*a-a*a-1 : p>1-d ? b*b+2*b+1 : 0; }
lira_osc(freq,duty) {
 History phase(0), width(0.53125), last(0), filt(0);
 f=abs(freq); dt=f/samplerate; p=phase; phase=wrap(p+dt,0,1);
 if(p<last){width=clamp(duty,0,1);} last=p;
 q=wrap(p+width,0,1);
 square=(2*p-1-lira_blep(p,dt))-(2*q-1-lira_blep(q,dt))+2*width-1;
 a=exp(-6.28318530718*clamp(max(f/4,100),0,samplerate/2)/samplerate);
 filt=(1-a)*square+a*filt;
 return square*0.59, filt*2.65-0.145;
}
lira_voice(arg_freq,arg_sharp,arg_gate,arg_hold,arg_fast,arg_duty) {
 envelope_value=lira_ramp(arg_gate,arg_gate>0 ? (arg_fast>0?100:200) : (arg_fast>0?100:8000));
 sq,tr=lira_osc(arg_freq,arg_duty);
 return (sq*arg_sharp+tr*(1-arg_sharp)+sin(envelope_value*6.28318530718)*0.5)*min(1,envelope_value*envelope_value+arg_hold);
}
lira_dynamics(x) {
 History env(0), sumsq(0);
 Delay rmsbuf(512);
 a=exp(-4.60517/(samplerate*0.0025)); env=abs(x)+a*(env-abs(x));
 gain=clamp(((env-0.2511886432)/5+0.2511886432)/max(env,0.0000000001),0,1);
 comp=x*lira_sat(gain);
 sq=comp*comp; old=rmsbuf.read(512); rmsbuf.write(sq);
 sumsq=max(0,sumsq+sq-old);
 db=10*log10(max(sumsq/512,0.000000000001));
 // 512-sample rectangular RMS approximation to Pd env~ Hann detector.
 eg=lira_ramp(pow(10,min(0,(db+60)*0.8)/20),11);
 return comp*eg;
}
'''
for n,l,v,m in params: code+=f'Param {n}({v},min=0,max={m});\n'
for i in range(1,9):code+=f'Param gate{i}(0,min=0,max=1);\n'
code+='Param extready(0,min=0,max=1);\n'
code+='''
Delay pair1(64),pair2(64),pair3(64),pair4(64),totaldelay(64);
Delay delay1(1048576),delay2(1048576);
History lphase1(0),lphase2(0);
History pair_state1(0),pair_state2(0),pair_state3(0),pair_state4(0),total_state(0);
fla=lira_ramp(mtof(pow(lfo1/127,2)*127-75),23.22);
flb=lira_ramp(mtof(pow(lfo2/127,2)*127-75),23.22);
ls1=clamp(cos(lphase1*6.28318530718)*1000,-1,1);
ls2=clamp(cos(lphase2*6.28318530718)*1000,-1,1);
ltri=((abs(lphase1-0.5)*4-1)+(abs(lphase2-0.5)*4-1))*0.5;
lsqr=(ls1+ls2)*0.5;
lmod=andor>0 ? lsqr : ls1*ls2;
lphase1=wrap(lphase1+fla/samplerate,0,1);
lphase2=wrap(lphase2+(flb+ls1*flb*0.5*link)/samplerate,0,1);
p1=pair_state1; p2=pair_state2; p3=pair_state3; p4=pair_state4; tf=total_state;
pair_state1=pair1.read(63);pair_state2=pair2.read(63);pair_state3=pair3.read(63);pair_state4=pair4.read(63);total_state=totaldelay.read(63);
'''
tuning=[(-16,93),(-16,93),(7,109),(9,107),(20,116.54),(20,116.54),(33,126.24),(33,131.22)]
for p,(a,b) in enumerate([(2,4),(1,1),(4,2),(3,3)],1):
 code+=f'''src{p}=((routing>0?0.001:1)*p{a}+(routing>0?1:0.001)*p{b})*(source{p}==0?1:0.001)+(lmod*(totalfb>0?0.001:1)+tf*(totalfb>0?1:0.001))*(source{p}==2?1:0.001);
md{p}=lira_ramp(pow(mod{p}/127,4)*2,23.22); sh{p}=lira_ramp(pow(sharp{p}/127,2),23.22);
vib{p}=cycle({[1.13,2.31,3.17,1.79][p-1]})*lira_ramp(vibrato,23.22);
'''
for i,(lo,hi) in enumerate(tuning,1):
 p=(i+1)//2;g=1 if i<=4 else 2
 code+=f'''raw{i}=mtof({lo}+tune{i}/127*{hi-lo})*(0.01+1.99*pitch{g}/127);
fq{i}=lira_ramp(quantize>0?mtof(floor(ftom(raw{i})+0.5)):raw{i},23.22);
v{i}=lira_voice(fq{i}*(1+vib{p}*0.005)*(1+src{p}*md{p}),sh{p},max(gate{i},voiceon{i}),lira_ramp(pow(hold{g}/127,2),23.22),fast{p},0.53125+vib{p}*0.025);
'''
for p in range(1,5):code+=f'pair{p}.write(lira_hp(v{2*p-1}+v{2*p},3));\n'
code+='''
dry=(v1+v2+v3+v4+v5+v6+v7+v8)*0.166667;
dry=dry+(in1+in2)*0.5*lira_ramp(extgain/127*extready,23.22);
fb=lira_ramp(feedback/127*pow(2,2*feedback/127),23.22);
dlfo=(dwave>0?lsqr:ltri)*(dsource==2);
self1=lira_lp(delay1.read(64)*0.5*(dsource==0),689);
self2=lira_lp(delay2.read(64)*0.5,689)*(dsource==0);
ms1=lira_ramp(pow(2,time1/127*12)*1.45125,23.22)+(self1+dlfo)*lira_ramp(pow(dmod1/127,2)*10,23.22);
ms2=lira_ramp(pow(2,time2/127*12)*1.45125,23.22)+(self2+dlfo)*lira_ramp(pow(dmod2/127,2)*10,23.22);
d1=lira_dynamics(lira_lp(lira_hp(delay1.read(clamp(ms1*samplerate/1000,64,1048575),interp="cubic"),1),4000));
d2=lira_dynamics(lira_lp(lira_hp(delay2.read(clamp(ms2*samplerate/1000,64,1048575),interp="cubic"),1),4000));
n=noise()*0.001;
delay1.write(dry+n+d1*fb);delay2.write(dry+n+d2*fb);
wet=lira_sat((d1+d2)*0.5/max(fb,1.5));
dm=lira_ramp(dmix/127,23.22); mixed=dry*(1-dm)+wet*dm;
dg=lira_ramp(pow(10,(pow(3,1+2*drive/127)+3)/20),23.22);
dist=lira_sat(lira_hp(mixed*dg,20));
dist=lira_hp(dist+pow(dist,31)*0.25,10)/clamp(dg,1,4)+mixed*0.1;
mixd=lira_ramp(distmix/127,23.22);
master=lira_sat(mixed*(1-mixd)+dist*mixd);
totaldelay.write(lira_hp(master,3));
out1=master*lira_ramp(pow(volume/127,2),23.22);
out2=out1;
'''
from inline_filters import inline_filters
code = inline_filters(code)
(OUT/'LIRA-engine.genexpr').write_text(code)
boxes=[];lines=[]
def box(id,cls='newobj',text=None,rect=None,**kw):
 b=dict(id=id,maxclass=cls,patching_rect=rect or [20,250+len(boxes)*25,160,22],**kw)
 if text is not None:b['text']=text
 boxes.append({'box':b});return id
def wire(a,b,ao=0,bi=0):lines.append({'patchline':{'source':[a,ao],'destination':[b,bi]}})
gp={'fileversion':1,'classnamespace':'dsp.gen','rect':[0,0,900,650],'boxes':[{'box':{'id':'code','maxclass':'codebox','code':code,'numinlets':2,'numoutlets':2,'patching_rect':[20,20,850,600]}}],'lines':[]}
for i in [1,2]:gp['boxes'].append({'box':{'id':f'out{i}','maxclass':'newobj','text':f'out {i}','patching_rect':[i*100,640,50,22]}});gp['lines'].append({'patchline':{'source':['code',i-1],'destination':[f'out{i}',0]}})
for i in [1,2]:gp['boxes'].append({'box':{'id':f'in{i}','maxclass':'newobj','text':f'in {i}','patching_rect':[i*100,0,50,22],'numinlets':0,'numoutlets':1}});gp['lines'].append({'patchline':{'source':[f'in{i}',0],'destination':['code',i-1]}})
box('engine',text='gen~',patcher=gp,numinlets=2,numoutlets=2,outlettype=['signal','signal'])
box('audioinput',text='plugin~ 1 2',numinlets=2,numoutlets=2,outlettype=['signal','signal']);wire('audioinput','engine');wire('audioinput','engine',1,1)
box('output',text='plugout~',numinlets=2,numoutlets=0);wire('engine','output');wire('engine','output',1,1)
box('title','comment','LIRA • 8   /   Push port alpha',[8,8,350,20],presentation=1,presentation_rect=[8,8,350,20],fontsize=16)
box('hint','comment','MIDI 36–43 = voices 1–8. Hold sustains each group. Master starts low.',[360,8,550,20],presentation=1,presentation_rect=[360,8,550,20])
parameters={}
for j,(n,l,v,m) in enumerate(params):
 x=8+(j%12)*85;y=34+(j//12)*31
 box('lab_'+n,'comment',l,[x,y,84,16],presentation=1,presentation_rect=[x,y,84,16],fontsize=9)
 box(n,'live.numbox',rect=[x,y+14,76,15],presentation=1,presentation_rect=[x,y+14,76,15],numinlets=1,numoutlets=2,outlettype=['','float'],parameter_enable=1,varname=n,saved_attribute_attributes={'valueof':{'parameter_longname':l,'parameter_shortname':l,'parameter_type':0 if m==127 else 1,'parameter_mmin':0,'parameter_mmax':m,'parameter_initial_enable':1,'parameter_initial':[v],'parameter_unitstyle':0}})
 box('send_'+n,text='prepend '+n);wire(n,'send_'+n);wire('send_'+n,'engine');parameters[n]=[l,l,0]
box('notes',text='notein',numinlets=1,numoutlets=3)
box('notepack',text='pack 0 0');wire('notes','notepack');wire('notes','notepack',1,1)
box('route',text='route 36 37 38 39 40 41 42 43',numinlets=1,numoutlets=9);wire('notepack','route')
for i in range(1,9):
 box('on'+str(i),text='> 0');wire('route','on'+str(i),i-1)
 box('gate'+str(i),text='prepend gate'+str(i));wire('on'+str(i),'gate'+str(i));wire('gate'+str(i),'engine')
box('banks',text='live.banks')
bankgroups=[('Voice On',[f'voiceon{i}' for i in range(1,9)]),('Tune',[f'tune{i}' for i in range(1,9)]),('Tone',['sharp1','sharp2','sharp3','sharp4','mod1','mod2','mod3','mod4']),('Voices',['pitch1','pitch2','hold1','hold2','fast1','fast2','fast3','fast4']),('Routing',['source1','source2','source3','source4','routing','totalfb','vibrato','quantize']),('LFO',['lfo1','lfo2','link','andor','dsource','dwave','volume','dmix']),('Delay',['time1','time2','dmod1','dmod2','feedback','dmix','dsource','dwave']),('Output',['drive','distmix','volume','hold1','hold2','feedback','dmix','vibrato'])]
# Push banks resolve parameter Long Names, not object IDs / scripting names.
longnames={n:label for n,label,_,_ in params}
parameters['parameterbanks']={str(i):{'index':i,'name':name,'parameters':[longnames[n] for n in names]} for i,(name,names) in enumerate(bankgroups)}
parameters['inherited_shortname']=1
patch={'patcher':{'fileversion':1,'appversion':{'major':9,'minor':0,'revision':0,'architecture':'x64','modernui':1},'classnamespace':'box','rect':[0,0,1050,700],'openinpresentation':1,'devicewidth':1035,'default_fontsize':11,'default_fontname':'Arial','boxes':boxes,'lines':lines,'parameters':parameters,'dependency_cache':[]}}
from ui import apply_ui
apply_ui(patch['patcher'], params, ROOT)
from audio_input import add_audio_routing
add_audio_routing(patch['patcher'], ROOT)
data=json.dumps(patch,indent=2).encode()+b'\x00'
(OUT/'LIRA-Push.maxpat').write_bytes(data[:-1])
# Same instrument container chunks as Ableton's bundled Max Instrument template.
(OUT/'LIRA-Push.amxd').write_bytes(b'ampf'+struct.pack('<I',4)+b'iiii'+b'meta'+struct.pack('<II',4,0)+b'ptch'+struct.pack('<I',len(data))+data)
shutil.copy(ROOT/'License.txt',OUT/'License.txt')
print('Built',len(params),'parameters',len(code),'bytes of Gen code')
