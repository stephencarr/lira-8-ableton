"""Build an audio effect from the instrument's actual Hyper LFO/delay/output code.

Run build.py first. No LiveAPI or pad takeover is needed by this effect.
"""
import copy
import json
import pathlib
import re
import struct

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
base = json.loads((ROOT / 'build/LIRA-Push/LIRA-Push.maxpat').read_text())['patcher']
by = {e['box']['id']: e['box'] for e in base['boxes']}
source = by['engine']['patcher']['boxes'][0]['box']['code']
names = ['time1', 'time2', 'dmod1', 'dmod2', 'feedback', 'dmix', 'dsource', 'dwave',
         'lfo1', 'lfo2', 'link', 'drive', 'distmix', 'volume']

# Reuse the exact generated filter/functions, LFO, delay and distortion sections.
# The oscillators and their FM feedback network are intentionally not instantiated.
header = source[:source.index('Param tune1')]
lfo = source[source.index('fla=lira_ramp'):source.index('p1=pair_state1;')]
lfo = re.sub(r'^lmod=.*\n', '', lfo, flags=re.M)  # AND/OR only feeds voice FM.
tail = source[source.index('fb=lira_ramp'):]
tail = re.sub(r'^hpf_8_a = .*\n|^totaldelay\.write.*\n', '', tail, flags=re.M)
params = ''.join(re.search(r'^Param ' + n + r'\([^;]+;', source, re.M)[0] + '\n' for n in names)
params = params.replace('Param dmix(30,', 'Param dmix(127,')
code = (header + params + 'Param inputgain(127,min=0,max=127);\n'
        'Delay delay1(1048576),delay2(1048576);\nHistory lphase1(0),lphase2(0);\n' + lfo +
        'dry=(in1+in2)*0.5*lira_ramp(inputgain/127,23.22);\n' + tail)

boxes, lines, parameters = [], [], {}
BG = [.095, .075, .09, 1]
PANEL = [.16, .13, .155, 1]
TEXT = [.95, .92, .94, 1]
ACCENT = [.64, .73, .69, 1]

def add(i, cls='newobj', text=None, rect=None, **kw):
    b = dict(id=i, maxclass=cls, patching_rect=rect or [20, 240+len(boxes)*24, 180, 22], **kw)
    if text is not None:
        b['text'] = text
    boxes.append({'box': b})
    return b

def wire(a, b, ao=0, bi=0):
    lines.append({'patchline': {'source': [a, ao], 'destination': [b, bi]}})

def label(i, text, rect, size=11, color=TEXT):
    return add(i, 'comment', text, rect, presentation=1, presentation_rect=rect,
               fontsize=size, textcolor=color, fontname='Arial')

def panel(i, text, rect):
    add(i, 'panel', rect=rect, presentation=1, presentation_rect=rect, bgcolor=PANEL,
        rounded=8, border=0, background=1, ignoreclick=1)
    label(i+'label', text, [rect[0]+8, 9, rect[2]-16, 18], color=ACCENT)

label('brand', 'LIRA DELAY', [10, 8, 145, 26], 19, ACCENT)
label('description', 'DUAL MOD DELAY\n+ DISTORTION', [12, 40, 135, 34], 10)
label('routinghint', 'Insert or return\nReturn: Mix at 127\nStereo input → mono', [12, 98, 137, 58], 10)
panel('lfopanel', 'HYPER LFO', [154, 4, 140, 160])
panel('delaypanel', 'MOD DELAY', [300, 4, 278, 160])
panel('outpanel', 'INPUT / DISTORTION / OUT', [584, 4, 200, 160])
layout = {'lfo1':[164,32,56,55], 'lfo2':[228,32,56,55], 'link':[170,118,108,22],
          'dsource':[503,49,67,20], 'dwave':[503,109,67,20]}
for j, n in enumerate(['time1','time2','feedback','dmod1','dmod2','dmix']):
    layout[n] = [308+(j%3)*63, 31+(j//3)*65, 58, 55]
for j, n in enumerate(['inputgain','volume','drive','distmix']):
    layout[n] = [602+(j%2)*90, 31+(j//2)*65, 74, 55]
label('srclabel', 'MOD SOURCE', [503,30,70,16], 8)
label('wavelabel', 'LFO WAVE', [503,90,70,16], 8)

for n in names+['inputgain']:
    b = copy.deepcopy(by['volume' if n=='inputgain' else n])
    b.update(id=n, varname=n, presentation=1, presentation_rect=layout[n], patching_rect=layout[n])
    attrs = b['saved_attribute_attributes']['valueof']
    if n=='inputgain':
        attrs.update(parameter_longname='Input', parameter_shortname='Input', parameter_initial=[127])
        b['hint'] = 'Input gain. 127 = unity; 0 stops new audio entering the delay.'
    if n=='dmix':
        attrs['parameter_initial'] = [127]
        b['hint'] = 'Delay Mix: 0 dry, 127 wet. Use 127 on a return track.'
    if b['maxclass']=='live.dial':
        b.update(shownumber=0, activefgdialcolor=ACCENT)
    boxes.append({'box':b})
    longname = attrs['parameter_longname']
    parameters[n] = [longname, attrs['parameter_shortname'], 0]
    add('send_'+n, text='prepend '+n)
    wire(n, 'send_'+n); wire('send_'+n, 'engine')
    # Restore actual saved/automated values without banging toggle controls.
    add('read_'+n, text='pattr @bindto '+n+' @autorestore 0')
    wire('defer','read_'+n); wire('read_'+n,'send_'+n)

gp = copy.deepcopy(by['engine']['patcher'])
gp['boxes'][0]['box'].update(code=code, numinlets=2)
# The base synth now already declares its two audio inlets.
add('engine', text='gen~', patcher=gp, numinlets=2, numoutlets=2, outlettype=['signal','signal'])
add('input', text='plugin~', numinlets=2, numoutlets=2, outlettype=['signal','signal'])
add('output', text='plugout~', numinlets=2, numoutlets=0)
for i in [0,1]:
    wire('input','engine',i,i); wire('engine','output',i,i)
add('boot',text='live.thisdevice'); add('defer',text='deferlow'); wire('boot','defer')
add('banks',text='live.banks')
groups = [('Delay',names[:8]),
          ('Hyper LFO',['lfo1','lfo2','link','dsource','dwave','dmod1','dmod2','feedback']),
          ('Output',['inputgain','drive','distmix','volume','dmix','feedback','time1','time2'])]
parameters['parameterbanks'] = {str(i):dict(index=i,name=title,parameters=[parameters[n][0] for n in ns]) for i,(title,ns) in enumerate(groups)}
parameters['inherited_shortname'] = 1
p = dict(fileversion=1, appversion=base['appversion'], classnamespace='box', rect=[0,0,790,700],
         openinpresentation=1, devicewidth=790, bgcolor=BG, editing_bgcolor=BG,
         default_fontsize=11, default_fontname='Arial', boxes=boxes, lines=lines,
         parameters=parameters, dependency_cache=[])
raw = json.dumps({'patcher':p},indent=2).encode()+b'\0'
(OUT/'LIRA-Delay.maxpat').write_bytes(raw[:-1])
(OUT/'LIRA-Delay.amxd').write_bytes(b'ampf'+struct.pack('<I',4)+b'aaaa'+b'meta'+struct.pack('<II',4,0)+b'ptch'+struct.pack('<I',len(raw))+raw)
(OUT/'LIRA-Delay.genexpr').write_text(code)
print('Built LIRA Delay: native stereo input, mono dual delay, 15 parameters, three Push banks.')
