import json,struct,pathlib
p=pathlib.Path('build/LIRA-Push/LIRA-Push.amxd').read_bytes()
assert p[:12]==b'ampf\x04\x00\x00\x00iiii'
assert struct.unpack('<I',p[28:32])[0]==len(p)-32
j=json.loads(p[32:].rstrip(b'\0'))['patcher']
def check(g):
 ids=[b['box']['id'] for b in g['boxes']]
 assert len(ids)==len(set(ids))
 for l in g['lines']:
  for k in ['source','destination']:assert l['patchline'][k][0] in ids
 for b in g['boxes']:
  if 'patcher' in b['box']:check(b['box']['patcher'])
check(j)
live=[b['box'] for b in j['boxes'] if b['box'].get('parameter_enable')==1]
assert len(live)==55
names={b['saved_attribute_attributes']['valueof']['parameter_longname'] for b in live}
assert len(names)==55, 'Parameter Long Names must be unique'
assert names=={v[0] for k,v in j['parameters'].items() if k not in ('parameterbanks','inherited_shortname')}
for b in j['parameters']['parameterbanks'].values():
 assert len(b['parameters'])==8
 assert set(b['parameters'])<=names
gen=next(b['box'] for b in j['boxes'] if b['box']['id']=='engine')['patcher']
code=gen['boxes'][0]['box']['code']
assert code==pathlib.Path('build/LIRA-Push/LIRA-engine.genexpr').read_text()
for i in range(1,9):
 n=f'voiceon{i}'
 assert f'Param {n}(0,min=0,max=1);' in code
 assert f'max(gate{i},{n})' in code
 assert any(l['patchline']['source']==[n,0] and l['patchline']['destination']==['send_'+n,0] for l in j['lines'])
 assert any(l['patchline']['source']==['send_'+n,0] and l['patchline']['destination']==['engine',0] for l in j['lines'])
assert not j['dependency_cache']
print('PASS: container lengths, JSON, unique IDs, all patch-cord endpoints, 55 parameters, eight eight-slot banks, embedded source consistency.')
print('NOT TESTED: Max compilation, audio, Live state, Push standalone.')
