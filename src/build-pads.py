"""Build separate, self-contained pad edition from the working desktop instrument."""
import json,pathlib,struct,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'dist';OUT.mkdir(exist_ok=True)
p=json.loads((ROOT/'build/LIRA-Push/LIRA-Push.maxpat').read_text())['patcher']
boxes=p['boxes'];lines=p['lines'];by={e['box']['id']:e['box'] for e in boxes}
def add(i,cls='newobj',text=None,**kw):
 b=dict(id=i,maxclass=cls,patching_rect=[20,800,150,22],**kw)
 if text is not None:b['text']=text
 boxes.append({'box':b});return b
def wire(a,b,ao=0,bi=0):lines.append({'patchline':{'source':[a,ao],'destination':[b,bi]}})
groups=[]
for k in range(1,5):
 g=1 if k<3 else 2
 groups.append((f'Voices {2*k-1}-{2*k}',[f'tune{2*k-1}',f'tune{2*k}',f'mod{k}',f'sharp{k}',f'source{k}',f'fast{k}',f'pitch{g}',f'hold{g}']))
groups.extend([('Hyper LFO',['lfo1','lfo2','andor','link','vibrato','quantize','routing','totalfb']),('Delay',['time1','time2','dmod1','dmod2','feedback','dmix','dsource','dwave']),('Output',['drive','distmix','volume','extgain','extsource','exttap','dmix','padmode'])])
groups.append(('Voice Mixer',['level'+str(i) for i in range(1,9)]))
def parameter(n,label,initial,choices,rect):
 b=add(n,'live.menu',varname=n,parameter_enable=1,numinlets=1,numoutlets=3,outlettype=['','','float'],items=choices,presentation=1,presentation_rect=rect,saved_attribute_attributes={'valueof':{'parameter_longname':label,'parameter_shortname':label,'parameter_type':2,'parameter_enum':choices,'parameter_mmin':0,'parameter_mmax':len(choices)-1,'parameter_unitstyle':9,'parameter_initial_enable':1,'parameter_initial':[initial]}})
 p['parameters'][n]=[label,label,0];return b
parameter('padmode','Pad Control',1,['Off','On'],[10,146,62,18])
parameter('padpage','Pad Page',0,[x[0] for x in groups],[78,146,70,18])
parameter('padstatusvalue','Pad Status',0,['Starting','Off','Select LIRA','No Surface','No Matrix','Press Note','Ready','API Error'],[78,146,110,18])
next(e['box'] for e in boxes if e['box']['id']=='padpage')['presentation']=0
by['recallnote'].update(text='Pad control / status',presentation_rect=[10,124,139,17])
for i in range(1,9):
 n='level'+str(i);label='Voice '+str(i)+' Level'
 add(n,'live.dial',varname=n,parameter_enable=1,numinlets=1,numoutlets=2,outlettype=['','float'],presentation=0,saved_attribute_attributes={'valueof':{'parameter_longname':label,'parameter_shortname':label,'parameter_type':0,'parameter_mmin':0,'parameter_mmax':127,'parameter_initial_enable':1,'parameter_initial':[127]}})
 p['parameters'][n]=[label,label,0]
 add('send_'+n,text='prepend '+n);wire(n,'send_'+n);wire('send_'+n,'engine')
 add('padlevel'+str(i),text='prepend level '+str(i-1));wire(n,'padlevel'+str(i));wire('padlevel'+str(i),'padcontroller')
longnames={e['box']['id']:e['box']['saved_attribute_attributes']['valueof']['parameter_longname'] for e in boxes if e['box'].get('parameter_enable')}
pages=[dict(name=name,parameters=[longnames[n] for n in names]) for name,names in groups]
# Eight permanent banks: four voice pairs, LFO, Delay, Output, Mixer.
p['parameters']['parameterbanks']={str(i):dict(index=i,**page) for i,page in enumerate(pages)}
code=(ROOT/'src/pads.js').read_text().replace('__PAGES__',json.dumps(pages))
add('padcontroller','v8.codebox',code=code,filename='none',numinlets=1,numoutlets=4,outlettype=['','','',''],saved_object_attributes={'parameter_enable':0})
add('padboot',text='live.thisdevice');add('paddefer',text='deferlow');add('padinit','message','init')
add('padsettle',text='delay 500')
wire('padboot','paddefer');wire('paddefer','padsettle');wire('padsettle','padinit');wire('padinit','padcontroller')
add('padclose',text='closebang');add('padshutdown','message','shutdown');wire('padclose','padshutdown');wire('padshutdown','padcontroller')
add('padenable',text='prepend enable');wire('padmode','padenable');wire('padenable','padcontroller')
add('padpagenumber',text='prepend page');wire('padpage','padpagenumber');wire('padpagenumber','padcontroller')
wire('padcontroller','engine',3)
for i in range(8):
 add('padstate'+str(i),text='prepend state '+str(i));wire('voiceon'+str(i+1),'padstate'+str(i));wire('padstate'+str(i),'padcontroller')
 # Sync recalled Live state after initialization, not only parameter defaults.
 wire('paddefer','voiceon'+str(i+1))
wire('paddefer','padmode');wire('paddefer','padpage')
# Mixer initialization comes from the saved Live parameters via LiveAPI.
add('padroutes',text='route '+' '.join(['voiceon'+str(i) for i in range(1,9)]+['padpage','padstatusvalue']+['level'+str(i) for i in range(1,9)]),numinlets=1,numoutlets=19)
wire('padcontroller','padroutes')
for i,n in enumerate(['voiceon'+str(i) for i in range(1,9)]+['padpage','padstatusvalue']+['level'+str(i) for i in range(1,9)]):wire('padroutes',n,i)
# Query saved values through pattr: a bang into live.text would TOGGLE it.
control_ids=[n for n in longnames if n!='padstatusvalue']
for n in control_ids:
 add('padread_'+n,text='pattr @bindto '+n+' @autorestore 0')
 for edge in lines:
  pl=edge['patchline']
  if pl['destination']==[n,0] and pl['source'][0] in ('deferopen','openpanel','paddefer'):
   pl['destination']=['padread_'+n,0]
 if n.startswith('level'):
  pass
 elif n in ('padmode','padpage'):
  wire('padread_'+n,'padenable' if n=='padmode' else 'padpagenumber')
 else:
  wire('padread_'+n,'ui_set_'+n)
  if n.startswith('voiceon'):wire('padread_'+n,'padstate'+str(int(n[7:])-1))
# Mirror status and page selector in the desktop panel; still fully usable without Push.
add('padstatus','comment','Waiting for Live',presentation=0)
wire('padcontroller','padstatus',2)
wire('padcontroller','subtitle',2)
by['subtitle']['fontsize']=8
add('padstatussend',text='s #0-pad-status');wire('padcontroller','padstatussend',2)
popup=by['instrument']['patcher']
for entry in popup['boxes']:
 b=entry['box']
 if b['id']=='fullmidi':b.update(text='PADS: LATCHES + MIXER / DISPLAY BUTTONS: BANKS')
 if b['id']=='fullsubtitle':b.update(text='PAD EDITION · '+ 'eight voices / eight menu banks')
 if b['id']=='footer':b.update(text='Select LIRA on Push and press Note. Top row inactive. Display buttons select banks. Middle: voice levels. Second bottom: latches (dark = off). Bottom: pressure adds pitch + sharpness; notes 36–43.')
popup['boxes'].append({'box':dict(id='padstatusrecv',maxclass='newobj',text='r #0-pad-status',patching_rect=[10,800,150,22])})
popup['lines'].append({'patchline':{'source':['padstatusrecv',0],'destination':['fullmidi',0]}})
# Do not auto-open a desktop window when the standalone instrument loads.
lines[:]=[l for l in lines if not(l['patchline']['source'][0]=='deferopen' and l['patchline']['destination'][0]=='openmsg')]
by['brand']['text']='LIRA • PADS'
by['title']['text']='LIRA • 8 / Pad edition alpha 10 · Note tuning'
# Hybrid surface: native serial-note bottom row, seven grabbed UI rows.
p['is_mpe']=1
# Native note LEDs use the named colours supported by live.push; the custom
# latch/fader rows use the muted numeric palette in pads.js.
palette=['ocean','ocean','sky','sky','purple','purple','purple','purple']
add('pushlayout',text='live.push @play_usage first_or_selected @play_pad_map serial @play_in_tune_location finger @play_note_colors '+' '.join(palette[(n-36)%8] for n in range(128)))
add('pushserial','message','play_pad_map serial');wire('paddefer','pushserial');wire('pushserial','pushlayout')
# MPE parsing retains Live's voice identity rather than treating MIDI channels as voices.
lines[:]=[l for l in lines if l['patchline']['destination'][0]!='route']
add('expressin',text='midiin',numinlets=0,numoutlets=1)
add('expressparse',text='mpeparse @hires 1',numinlets=1,numoutlets=10)
add('expression','v8.codebox',code=(ROOT/'src/expression.js').read_text(),filename='none',numinlets=1,numoutlets=1,outlettype=[''],saved_object_attributes={'parameter_enable':0})
wire('expressin','expressparse')
for outlet,name in [(0,'note'),(1,'polypressure'),(4,'pressure'),(5,'bend'),(6,'mpevoice'),(7,'zonefirst'),(8,'zoneindex')]:
 add('express_'+name,text='prepend '+name);wire('expressparse','express_'+name,outlet);wire('express_'+name,'expression')
wire('expression','engine')
add('expressresetroute',text='route expressreset');wire('padroutes','expressresetroute',18);wire('expressresetroute','expressreset')
add('expressreset','message','reset');wire('paddefer','expressreset');wire('expressreset','expression')
# Add output-only mixer gains; oscillator FM taps stay pre-fader.
gen=by['engine']['patcher']['boxes'][0]['box']
original=gen['code'];modified=original
for i in range(1,9):
 at=modified.index('Param ')
 modified=modified[:at]+'Param level%d(127,min=0,max=127);\nParam bend%d(0,min=-48,max=48);\nParam press%d(0,min=0,max=1);\n'%(i,i,i)+modified[at:]
 pair=(i+1)//2
 modified=modified.replace('lira_voice(fq%d*'%i,'lira_voice(fq%d*pow(2,lira_ramp(bend%d,5)/12)*'%(i,i))
 modified=modified.replace('),sh%d,max(gate%d,'%(pair,i),'),clamp(sh%d+lira_ramp(press%d,10)*0.6,0,1),max(gate%d,'%(pair,i,i))
modified=modified.replace('dry=(v1+v2+v3+v4+v5+v6+v7+v8)*0.166667;', 'dry=('+ '+'.join('v%d*lira_ramp(level%d/127,23.22)'%(i,i) for i in range(1,9))+')*0.166667;')
assert modified.count('pow(2,lira_ramp(bend')==8
assert modified.count('lira_ramp(press')==8
gen['code']=modified
from tuning import add_tuning
add_tuning(p,ROOT)
(OUT/'LIRA-engine.genexpr').write_text(modified)
raw=json.dumps({'patcher':p},indent=2).encode()+b'\0'
(OUT/'LIRA-Push-Pads.maxpat').write_bytes(raw[:-1])
(OUT/'LIRA-Push-Pads.amxd').write_bytes(b'ampf'+struct.pack('<I',4)+b'iiii'+b'meta'+struct.pack('<II',4,0)+b'ptch'+struct.pack('<I',len(raw))+raw)
(OUT/'LIRA-Pads-controller.js').write_text(code)
(OUT/'pages.json').write_text(json.dumps(pages,indent=2))
shutil.copy(ROOT/'build/LIRA-Push/License.txt',OUT/'License.txt')
print('Built alpha 10; temporary note tuning, 69 saved parameters, eight permanent banks.')
