import json,pathlib,struct,hashlib
root=pathlib.Path(__file__).resolve().parents[1]
out=root/'dist'
raw=(out/'LIRA-Push-Pads.amxd').read_bytes()
assert raw[:12]==b'ampf\x04\0\0\0iiii'
assert struct.unpack('<I',raw[28:32])[0]==len(raw)-32
p=json.loads(raw[32:].rstrip(b'\0'))['patcher']
def check(g):
 boxes={e['box']['id']:e['box'] for e in g['boxes']}
 assert len(boxes)==len(g['boxes'])
 for e in g['lines']:
  l=e['patchline']
  for key in ('source','destination'):assert l[key][0] in boxes
  for key,attr in [('source','numoutlets'),('destination','numinlets')]:
   b=boxes[l[key][0]]
   if attr in b:assert l[key][1]<b[attr],l
 for b in boxes.values():
  if 'patcher' in b:check(b['patcher'])
check(p)
boxes={e['box']['id']:e['box'] for e in p['boxes']}
assert not p['dependency_cache']
live=[b for b in boxes.values() if b.get('parameter_enable')]
assert len(live)==66
names={b['saved_attribute_attributes']['valueof']['parameter_longname'] for b in live}
assert len(names)==66
pages=json.loads((out/'pages.json').read_text())
assert len(pages)==8
for page in pages:
 assert len(page['parameters'])==8
 assert set(page['parameters'])<=names
for l in p['lines']:
 pl=l['patchline']
 if pl['source'][0] in ('deferopen','openpanel','paddefer'):
  assert boxes[pl['destination'][0]]['maxclass']!='live.text','Reading switch state must not toggle it'
base=json.loads((root/'build/LIRA-Push/LIRA-Push.maxpat').read_text())['patcher']
engine=boxes['engine']['patcher']
base_engine=next(b['box']['patcher'] for b in base['boxes'] if b['box']['id']=='engine')
original=base_engine['boxes'][0]['box']['code']
modified=engine['boxes'][0]['box']['code']
# Remove only the requested extensions; all original synthesis code must match.
import re
neutral=re.sub(r'Param (?:level|bend|press)\d+\([^;]+;\n','',modified)
for i in range(1,9):
 pair=(i+1)//2
 neutral=neutral.replace('fq%d*pow(2,lira_ramp(bend%d,5)/12)*'%(i,i),'fq%d*'%i)
 neutral=neutral.replace('clamp(sh%d+lira_ramp(press%d,10)*0.6,0,1)'%(pair,i),'sh%d'%pair)
 neutral=neutral.replace('v%d*lira_ramp(level%d/127,23.22)'%(i,i),'v%d'%i)
assert neutral==original,'Unexpected change to synthesis engine'
assert p['is_mpe']==1
assert boxes['expressparse']['text']=='mpeparse @hires 1'
assert boxes['expression']['code']==(root/'src/expression.js').read_text()
assert boxes['padcontroller']['code']==(out/'LIRA-Pads-controller.js').read_text()
assert '/private/tmp' not in boxes['padcontroller']['code'],'No desktop diagnostic paths in shipped device'
assert 'require(' not in boxes['padcontroller']['code']
print('PASS: self-contained AMXD, recursive patch wiring, 66 unique parameters, all eight page mappings, non-toggling state sync, neutral extensions preserve original audio engine.')

for bank in p['parameters']['parameterbanks'].values():
 assert set(bank['parameters'])<=names

assert len(p['parameters']['parameterbanks'])==8
assert p['parameters']['parameterbanks']['0']['name']=='Voices 1-2'
assert p['parameters']['parameterbanks']['7']['name']=='Voice Mixer'
assert all(b['name']!='Setup' for b in p['parameters']['parameterbanks'].values())
assert '@play_usage first_or_selected' in boxes['pushlayout']['text']
assert boxes['pushserial']['text']=='play_pad_map serial'
assert "msg=['edit'" not in boxes['padcontroller']['code']

assert 'store_chosen_bank' not in boxes['padcontroller']['code']
assert boxes['padsettle']['text']=='delay 500'
assert boxes['padpage']['presentation']==0

assert all(b['name']!='Perform' for b in p['parameters']['parameterbanks'].values())
