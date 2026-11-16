"""Build a silent desktop Live test of the real tuning patch and saved parameters."""
import json,math,pathlib,struct
root=pathlib.Path(__file__).resolve().parents[1]
p=json.loads((root/'dist/LIRA-Push-Pads.maxpat').read_text())['patcher']
ranges=[(-16,93),(-16,93),(7,109),(9,107),(20,116.54),(20,116.54),(33,126.24),(33,131.22)]
notes=[48,52,55,60,64,67,72,76]
by={e['box']['id']:e['box'] for e in p['boxes']}
for i,((lo,hi),note) in enumerate(zip(ranges,notes),1):
    by['tune'+str(i)]['saved_attribute_attributes']['valueof']['parameter_initial']=[127*(note-lo-12*math.log2(.01+1.99*63/127))/(hi-lo)]
by['padmode']['saved_attribute_attributes']['valueof']['parameter_initial']=[0]
p['lines']=[e for e in p['lines'] if e['patchline']['destination'][0]!='output']
def add(i,text=None,cls='newobj',**kw):
    b=dict(id=i,maxclass=cls,patching_rect=[20,1200,300,22],**kw)
    if text is not None:b['text']=text
    p['boxes'].append({'box':b})
def wire(a,b,o=0):p['lines'].append({'patchline':dict(source=[a,o],destination=[b,0])})
add('testsilence','sig~ 0');wire('testsilence','output')
p['lines'].append({'patchline':dict(source=['testsilence',0],destination=['output',1])})
script=r'''
inlets=1;outlets=0;var stage=0,rows=[],refs={},dsp={};var job=new Task(run,this);
function anything(){if(arguments.length)dsp[messagename]=Number(arguments[0]);}
function bang(){job.schedule(1500);}
function run(){try{
 if(stage===0){var d=new LiveAPI(null,'this_device'),ps=d.get('parameters');
  for(var i=0;i<ps.length;i++)if(ps[i]==='id'){var a=new LiveAPI(null,'id '+ps[++i]),name=String(a.get('name'));if(/^Pitch 1/.test(name))name='Pitch 1234';if(/^Pitch 5/.test(name))name='Pitch 5678';if(/^(Tune [1-8]|Pitch (1234|5678))$/.test(name))refs[name]=a;}}
 var row={stage:stage,parameters:{},dsp:JSON.parse(JSON.stringify(dsp))};
 Object.keys(refs).forEach(function(n){var a=refs[n],v=Number(a.get('value')[0]);row.parameters[n]={value:v,label:a.call('str_for_value',v)};});rows.push(row);
 var f=new File('__CAPTURE__','write','TEXT');f.eof=0;f.writestring(JSON.stringify(rows));f.close();
 var tuner=this.patcher.getnamed('notetuner');
 if(stage===0)tuner.message('manual',1);
 if(stage===1)for(var i=1;i<=8;i++)this.patcher.getnamed('tune'+i).message(Number(refs['Tune '+i].get('value')[0])+0.01);
 if(stage===2)this.patcher.getnamed('pitch1').message(Number(refs['Pitch 1234'].get('value')[0])+0.01);
 if(stage===3)tuner.message('manual',0);
 if(stage===4)this.patcher.getnamed('tune1').message(Number(refs['Tune 1'].get('value')[0])+0.123);
 if(stage<5){stage++;job.schedule(200);}
 }catch(e){post('Tuning test: '+e+'\n');}}
'''.replace('__CAPTURE__',str(root/'build/tuning-capture.json'))
add('testprobe',cls='v8.codebox',code=script,filename='none',numinlets=1,numoutlets=0)
wire('tuneinitdefer','testprobe');wire('notetuner','testprobe')
r=json.dumps({'patcher':p}).encode()+b'\0'
(root/'build/LIRA-Tuning-Test.amxd').write_bytes(b'ampf'+struct.pack('<I',4)+b'iiii'+b'meta'+struct.pack('<II',4,0)+b'ptch'+struct.pack('<I',len(r))+r)
print('Load build/LIRA-Tuning-Test.amxd in Live; check capture after four seconds. No speaker output.')
