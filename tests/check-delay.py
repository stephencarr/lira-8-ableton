import json
import pathlib
import re
import struct

root = pathlib.Path(__file__).resolve().parents[1]
raw = (root/'dist/LIRA-Delay.amxd').read_bytes()
assert raw[:12] == b'ampf\x04\0\0\0aaaa'
assert struct.unpack('<I',raw[28:32])[0] == len(raw)-32
p = json.loads(raw[32:].rstrip(b'\0'))['patcher']
b = {e['box']['id']:e['box'] for e in p['boxes']}
edges = [(e['patchline']['source'],e['patchline']['destination']) for e in p['lines']]
for i in [0,1]:
    assert (['input',i],['engine',i]) in edges
    assert (['engine',i],['output',i]) in edges
assert b['input']['text'] == 'plugin~'
assert b['output']['text'] == 'plugout~'
assert len([x for x in b.values() if x.get('parameter_enable')]) == 15
names = {x['saved_attribute_attributes']['valueof']['parameter_longname'] for x in b.values() if x.get('parameter_enable')}
for bank in p['parameters']['parameterbanks'].values():
    assert len(bank['parameters']) == 8 and set(bank['parameters']) <= names
assert b['dmix']['saved_attribute_attributes']['valueof']['parameter_initial'] == [127]
for n in p['parameters']:
    if n not in ('parameterbanks','inherited_shortname'):
        assert (['read_'+n,0],['send_'+n,0]) in edges
assert not p['dependency_cache']
assert not any(x['maxclass']=='v8.codebox' for x in b.values())
code = b['engine']['patcher']['boxes'][0]['box']['code']
assert code == (root/'dist/LIRA-Delay.genexpr').read_text()
assert 'dry=(in1+in2)*0.5*lira_ramp(inputgain/127,23.22);' in code
assert 'Param inputgain(127,min=0,max=127);' in code
original = (root/'build/LIRA-Push/LIRA-engine.genexpr').read_text()
tail = original[original.index('fb=lira_ramp'):]
tail = re.sub(r'^hpf_8_a = .*\n|^totaldelay\.write.*\n','',tail,flags=re.M)
assert code[code.index('fb=lira_ramp'):] == tail, 'Delay/output must remain identical to instrument'
def check(g):
    boxes = {e['box']['id']:e['box'] for e in g['boxes']}
    assert len(boxes) == len(g['boxes'])
    for e in g['lines']:
        for endpoint,attr in [('source','numoutlets'),('destination','numinlets')]:
            id,port = e['patchline'][endpoint]
            assert id in boxes
            if attr in boxes[id]: assert port < boxes[id][attr]
    for box in boxes.values():
        if 'patcher' in box: check(box['patcher'])
check(p)
print('PASS: effect container, stereo host input/output, 15 saved controls, three banks, and exact shared delay/distortion DSP.')
