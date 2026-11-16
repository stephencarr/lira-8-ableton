import copy,re,pathlib
PINK=[.973,.643,.769,1];INK=[.08,.065,.08,1];BG=[.12,.105,.12,1];PANEL=[.19,.165,.19,1];WHITE=[.96,.93,.94,1]
def apply_ui(p,params,root):
 boxes=p['boxes'];lines=p['lines'];by={b['box']['id']:b['box'] for b in boxes}
 def add(i,cls,text=None,rect=None,**kw):
  b=dict(id=i,maxclass=cls,patching_rect=rect or [20,350,100,22],**kw)
  if text is not None:b['text']=text
  boxes.append({'box':b});return b
 def wire(a,b,ao=0,bi=0):lines.append({'patchline':{'source':[a,ao],'destination':[b,bi]}})
 def visual(i,cls,rect,**kw):return add(i,cls,rect=rect,presentation=1,presentation_rect=rect,**kw)
 def label(i,text,rect,size=11,color=WHITE):return visual(i,'comment',rect,text=text,fontsize=size,textcolor=color,fontname='Arial')
 def panel(i,title,rect):
  visual(i,'panel',rect,bgcolor=PANEL,rounded=8,border=0)
  label(i+'title',title,[rect[0]+8,rect[1]+5,rect[2]-16,18],11,PINK)
 # Keep parameter IDs and all audio wiring stable.
 for b in boxes:
  if b['box'].get('presentation'):b['box']['presentation']=0
 p.update(devicewidth=1440,bgcolor=BG,editing_bgcolor=BG)
 # Draw backgrounds before controls.
 old=boxes[:];boxes.clear()
 visual('surface','panel',[0,0,1440,169],bgcolor=BG,border=0)
 label('brand','LIRA • 8',[10,8,140,25],20,PINK)
 label('subtitle','ORGANISMIC SYNTH',[10,35,140,16],9)
 layout={};short={};full={}
 for k in range(4):
  x=160+k*126;panel('pairpanel'+str(k),f'VOICES {k*2+1} / {k*2+2}',[x,4,120,160])
  for j in range(2):layout['tune'+str(2*k+j+1)]=[x+7+j*55,26,50,46];short['tune'+str(2*k+j+1)]=f'Tune {2*k+j+1}'
  for j,n in enumerate(['mod','sharp']):layout[n+str(k+1)]=[x+7+j*55,94,50,40];short[n+str(k+1)]=n.title()
  layout['source'+str(k+1)]=[x+6,139,71,18];layout['fast'+str(k+1)]=[x+80,139,34,18]
  for j in range(2):layout['voiceon'+str(2*k+j+1)]=[x+6+j*56,74,54,17]
 panel('grouppanel','PITCH / HOLD',[670,4,152,160])
 for j,n in enumerate(['pitch1','hold1','pitch2','hold2']):layout[n]=[679+(j%2)*70,28+(j//2)*67,62,60];short[n]=('Pitch ' if 'pitch' in n else 'Hold ')+('1–4' if n[-1]=='1' else '5–8')
 panel('lfopanel','HYPER LFO',[828,4,142,160])
 for j,n in enumerate(['lfo1','lfo2']):layout[n]=[838+j*65,29,58,64];short[n]='Rate '+('A' if j==0 else 'B')
 layout['andor']=[837,105,60,20];layout['link']=[901,105,60,20]
 layout['vibrato']=[837,137,60,19];layout['quantize']=[901,137,60,19]
 panel('delaypanel','MOD DELAY',[976,4,282,160])
 for j,n in enumerate(['time1','time2','feedback','dmod1','dmod2','dmix']):layout[n]=[984+(j%3)*63,27+(j//3)*65,58,59];short[n]={'time1':'Time 1','time2':'Time 2','feedback':'Feedback','dmod1':'Mod 1','dmod2':'Mod 2','dmix':'Mix'}[n]
 layout['dsource']=[1179,42,71,20];layout['dwave']=[1179,88,71,20]
 label('dsrc_label','MOD SOURCE',[1179,25,75,15],8);label('dwav_label','LFO WAVE',[1179,71,75,15],8)
 layout['routing']=[1179,116,71,18];layout['totalfb']=[1179,139,71,18]
 panel('distpanel','DISTORTION / OUT',[1264,4,170,160])
 for j,n in enumerate(['drive','distmix','volume']):layout[n]=[1272+(j%2)*78,29+(j//2)*67,68,60];short[n]={'drive':'Drive','distmix':'Mix','volume':'Master'}[n]
 layout['extgain']=[1350,96,68,60];short['extgain']='Audio In'
 layout['extsource']=[10,900,200,20];layout['exttap']=[220,900,130,20]
 boxes.extend(old)
 menus={**{f'source{i}':['Pair','Off','LFO / FB'] for i in range(1,5)},'andor':['AND','OR'],'dsource':['Self','Off','LFO'],'dwave':['Triangle','Square']}
 menus['extsource']=['Off','Input 1','Input 2','Input 1/2']+[f'Track {i}' for i in range(1,65)]
 menus['exttap']=['Pre FX','Post FX','Post Mixer']
 toggles={**{f'voiceon{i}':f'Voice {i} On' for i in range(1,9)},**{f'fast{i}':'Fast' for i in range(1,5)},'link':'Link','vibrato':'Vibrato','quantize':'Quantize','routing':'Route swap','totalfb':'Total FB'}
 def style_control(b,n,rect,labelname,enabled=True):
  b.update(presentation=1,presentation_rect=rect,patching_rect=rect,fontsize=10,parameter_enable=int(enabled))
  if n in menus:
   b.update(maxclass='live.menu',numoutlets=3,outlettype=['','', 'float'],items=menus[n],activebgcolor=PANEL,activetextcolor=WHITE)
  elif n in toggles:
   b.update(maxclass='live.text',mode=1,text=toggles[n].replace(' On',' Off'),texton=toggles[n],activebgcolor=[.29,.26,.29,1],activebgoncolor=PINK,activetextcolor=WHITE,activetextoncolor=INK,bgcolor=[.29,.26,.29,1],bgoncolor=PINK,textcolor=WHITE,textoncolor=INK,numoutlets=2,outlettype=['',''])
  else:b.update(maxclass='live.dial',appearance=0,showname=1,shownumber=1,activefgdialcolor=PINK,activeneedlecolor=WHITE,activebgcolor=[.3,.27,.3,1],textcolor=WHITE,activefgcolor=WHITE)
  attrs=b.setdefault('saved_attribute_attributes',{}).setdefault('valueof',{})
  attrs['parameter_shortname']=labelname
  if n in menus:attrs.update(parameter_type=2,parameter_enum=menus[n],parameter_unitstyle=9)
 for n,l,v,m in params:
  style_control(by[n],n,layout[n],short.get(n,l));by[n]['hint']=l+' — '+('0–127, same scale as Pure Data' if m==127 else 'Select '+l)
 by['extsource']['presentation']=0;by['exttap']['presentation']=0
 by['extgain']['hint']='External audio level: 0 muted, 127 unity. Select the source in the full panel or Push Output bank.'
 # Full window with mirrored controls. Native Max only: no JS or external graphics.
 popup={'fileversion':1,'classnamespace':'box','rect':[80,70,1064,658],'openinpresentation':1,'bgcolor':BG,'editing_bgcolor':BG,'boxes':[],'lines':[],'default_fontname':'Arial','default_fontsize':12}
 mainboxes,mainlines=boxes,lines;boxes=popup['boxes'];lines=popup['lines']
 add('window_inlet','inlet',numinlets=0,numoutlets=1)
 visual('fullbg','panel',[0,0,1064,658],bgcolor=BG,border=0)
 label('fullbrand','LIRA • 8',[20,12,230,36],28,PINK)
 label('fullsubtitle','Eight voices · four interacting pairs',[260,21,350,24],14)
 visual('fullclose','textbutton',[990,4,58,22],text='Close',fontsize=11,active=1,legacytextcolor=1,usegradient=0,bgcolor=PANEL,textcolor=WHITE,mode=0)
 add('closemessage','message','wclose');add('windowcontrol','newobj','thispatcher');wire('fullclose','closemessage');wire('closemessage','windowcontrol')
 label('fullmidi','LATCH VOICES ON BELOW  /  MIDI OPTIONAL',[705,25,340,18],11,PINK)
 panel('fulllfo','HYPER LFO',[16,54,240,158]);panel('fulldelay','MOD DELAY',[272,54,500,158]);panel('fulldist','DISTORTION / OUTPUT',[788,54,260,158])
 for j,n in enumerate(['lfo1','lfo2']):full[n]=[38+j*110,83,80,60]
 full['andor']=[36,173,94,24];full['link']=[144,173,92,24]
 for j,n in enumerate(['time1','time2','feedback','dmod1','dmod2','dmix']):full[n]=[287+(j%3)*93,80+(j//3)*62,82,60]
 full['dsource']=[582,102,170,26];full['dwave']=[582,172,170,26]
 label('modsrc','MODULATION SOURCE',[582,80,170,20],11);label('wave','LFO WAVEFORM',[582,150,170,20],11)
 for j,n in enumerate(['drive','distmix','volume']):full[n]=[799+j*81,105,75,60]
 panel('group14','VOICES 1–4',[16,224,386,86]);panel('global','GLOBAL',[416,224,232,86]);panel('group58','VOICES 5–8',[662,224,386,86])
 for j,n in enumerate(['pitch1','hold1','pitch2','hold2']):full[n]=[(35 if j<2 else 681)+(j%2)*176,247,156,60]
 for j,n in enumerate(['quantize','vibrato','routing','totalfb']):full[n]=[429+(j%2)*106,249+(j//2)*29,100,24]
 for k in range(4):
  x=16+k*262;panel('fullpair'+str(k),f'VOICE PAIR {k*2+1} / {k*2+2}',[x,322,246,218])
  for j in range(2):
   n='tune'+str(2*k+j+1);full[n]=[x+18+j*116,349,94,60]
   full['voiceon'+str(2*k+j+1)]=[x+18+j*116,412,94,23]
  for j,n in enumerate(['mod','sharp']):full[n+str(k+1)]=[x+18+j*116,442,94,60]
  label('sourcelabel'+str(k),'SOURCE',[x+15,513,70,18],10)
  full['source'+str(k+1)]=[x+91,510,71,24];full['fast'+str(k+1)]=[x+174,510,58,24]
 panel('fullaudio','EXTERNAL AUDIO → VOICES + DELAY + TOTAL FEEDBACK',[16,548,1032,78])
 full['extgain']=[30,567,90,56];full['extsource']=[146,586,200,24];full['exttap']=[368,586,150,24]
 label('extsourcelabel','AUDIO FROM',[146,566,200,18],11);label('exttaplabel','TRACK TAP',[368,566,150,18],11)
 label('audio_status','Audio input off',[540,586,490,24],12)
 label('footer','Tune sets each voice’s pitch. Mod, Sharp, Source and Fast are shared by the pair. Off releases a voice; Hold can keep its group sounding.',[20,634,1020,22],12)
 for n,l,v,m in params:
  rect=full[n];x,y,w,h=rect
  if n in menus:
   b=visual('ui_'+n,'umenu',rect,items=[item for j,value in enumerate(menus[n]) for item in ([',',value] if j else [value])],numinlets=1,numoutlets=3,outlettype=['int','',''],bgcolor=PANEL,textcolor=WHITE,fontsize=12)
  elif n in toggles:
   caption=toggles[n]
   offcaption=caption.replace(' On',' Off') if n.startswith('voiceon') else caption+' Off'
   oncaption=caption if n.startswith('voiceon') else caption+' On'
   b=visual('ui_'+n,'textbutton',rect,text=offcaption,texton=oncaption,mode=1,active=1,legacytextcolor=1,usegradient=0,usebgoncolor=1,fontsize=11,bgcolor=[.29,.26,.29,1],bgoncolor=PINK,textcolor=WHITE,textoncolor=INK,numinlets=1,numoutlets=3,outlettype=['int','','int'])
  else:
   label('label_'+n,short.get(n,l),[x,y,w,18],12)
   diameter=36
   b=visual('ui_'+n,'dial',[x+(w-diameter)/2,y+20,diameter,diameter],numinlets=1,numoutlets=1,outlettype=['float'],size=m+1,min=0,floatoutput=1,mode=5,outlinecolor=[.4,.35,.4,1],bgcolor=PANEL,needlecolor=PINK)
  add('recv_'+n,'newobj','r #0-state-'+n);wire('recv_'+n,'ui_'+n)
  add('send_'+n,'newobj','s #0-ui-'+n);wire('ui_'+n,'send_'+n)
  add('initial_'+n,'newobj','loadmess set '+str(v));wire('initial_'+n,'ui_'+n)

 boxes,lines=mainboxes,mainlines
 add('instrument','newobj','p Instrument',patcher=popup,numinlets=1,numoutlets=0)
 visual('openpanel','textbutton',[10,60,137,28],text='Open instrument',fontsize=12,bgcolor=PINK,textcolor=INK,mode=0,active=1,legacytextcolor=1,usegradient=0)
 add('openmsg','message','open');add('panelcontrol','newobj','pcontrol');wire('openpanel','openmsg');wire('openmsg','panelcontrol');wire('panelcontrol','instrument')
 add('autoopen','newobj','loadbang');add('deferopen','newobj','deferlow');wire('autoopen','deferopen');wire('deferopen','openmsg')
 for n,l,v,m in params:
  wire('deferopen',n);wire('openpanel',n)
  add('ui_recv_'+n,'newobj','r #0-ui-'+n);wire('ui_recv_'+n,n)
  add('ui_set_'+n,'newobj','prepend set');add('ui_state_'+n,'newobj','s #0-state-'+n);wire(n,'ui_set_'+n);wire('ui_set_'+n,'ui_state_'+n)
 # Recall the user's actual saved Pd values, keeping their listening level.
 names=[f'tune{i}' for i in range(1,9)]+[f'{n}{i}' for n in ['fast','sharp','mod','source'] for i in range(1,5)]+['pitch1','pitch2','hold1','hold2','routing','totalfb','vibrato','drive','distmix','volume','lfo1','lfo2','andor','link','time1','time2','feedback','dmix','dmod1','dmod2','dsource','dwave','quantize']
 values=[float(v.strip().strip(';')) for v in (root/'assets/pd-preset.txt').read_text().splitlines()]
 visual('pdrecall','textbutton',[10,97,137,24],text='PD saved patch',fontsize=11,bgcolor=PANEL,textcolor=WHITE,mode=0,active=1,legacytextcolor=1,usegradient=0)
 add('pdtrigger','newobj','t b');wire('pdrecall','pdtrigger')
 for n,v in zip(names,values):
  if n=='volume':continue
  add('pd_'+n,'message',str(v));wire('pdtrigger','pd_'+n);wire('pd_'+n,n)
 label('recallnote','Recall leaves Master\nunchanged.',[12,125,137,32],9)

 for collection in [boxes,popup['boxes']]:
  for entry in collection:
   if entry['box']['maxclass']=='panel':entry['box'].update(background=1,ignoreclick=1)
  collection.sort(key=lambda entry:(entry['box']['maxclass']=='panel',entry['box'].get('presentation_rect',[0,0,0,0])[2]*entry['box'].get('presentation_rect',[0,0,0,0])[3] if entry['box']['maxclass']=='panel' else 0))
 p['boxes']=boxes;p['lines']=lines
 return dict(zip(names,values))
