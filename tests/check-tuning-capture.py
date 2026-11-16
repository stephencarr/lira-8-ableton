"""Verify real Live parameter writeback, display labels, DSP messages and release."""
import json,math,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
rows=json.loads((root/'build/tuning-capture.json').read_text())
assert len(rows)==6,'Host test did not complete'
ranges=[(-16,93),(-16,93),(7,109),(9,107),(20,116.54),(20,116.54),(33,126.24),(33,131.22)]
notes=[48,52,55,60,64,67,72,76]
def value(stage,name):return rows[stage]['parameters'][name]['value']
def midi(stage,i):
    lo,hi=ranges[i]
    return lo+value(stage,f'Tune {i+1}')/127*(hi-lo)+12*math.log2(.01+1.99*value(stage,'Pitch 1234' if i<4 else 'Pitch 5678')/127)
for i in range(8):
    n=f'Tune {i+1}'
    assert value(0,n)==value(1,n),'Holding Shift retuned a voice'
    assert abs(midi(2,i)-notes[i]-1)<.0001,(i,midi(2,i))
    assert abs(midi(3,i)-notes[i]-(2 if i<4 else 1))<.0001
    assert value(3,n)==value(4,n),'Releasing Shift changed tuning'
    assert abs(value(2,n)-rows[2]['dsp'][f'tune{i+1}'])<.00002,'Saved value differs from DSP'
    assert isinstance(rows[2]['parameters'][n]['label'],str)
    assert not isinstance(rows[4]['parameters'][n]['label'],str) or not any(c in rows[4]['parameters'][n]['label'] for c in 'ABCDEFG')
assert abs(value(5,'Tune 1')-value(4,'Tune 1')-.123)<.00002
print('PASS: Live loaded the tuning engine; all eight voices snapped accurately, labels changed, saved parameters matched DSP, group transposition preserved intervals, release restored continuous tuning.')
print(json.dumps({'note_label':rows[2]['parameters']['Tune 1'],'released':rows[4]['parameters']['Tune 1']},indent=2))
