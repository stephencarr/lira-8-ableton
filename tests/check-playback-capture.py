"""Verify audible output for all eight latches and eight MIDI notes in Live."""
import array,json,math,pathlib,sys,wave
root=pathlib.Path(__file__).resolve().parents[1]
with wave.open(str(root/'build/playback-capture.wav'),'rb') as w:
    sr=w.getframerate();assert w.getnchannels()==2 and w.getsampwidth()==2
    assert w.getnframes()>sr*17.8,'Capture has not completed'
    a=array.array('h',w.readframes(w.getnframes()))
if sys.byteorder!='little':a.byteswap()
left=a[::2];right=a[1::2]
def rms(lo,hi):
    c=left[int(lo*sr):int(hi*sr)]
    return math.sqrt(sum(v*v for v in c)/len(c))/32768
baseline=rms(.1,.4);rows=[]
for stage in range(16):
    start=.5+stage
    energy=rms(start+.25,start+.55)
    assert energy>.002 and energy>baseline*8,('silent voice',stage,energy,baseline)
    rows.append(dict(mode='Latch' if stage<8 else 'MIDI',voice=stage%8+1,rms=energy))
assert left==right,'Original mono synthesis should agree on both outputs'
peak=max(map(abs,a))/32768
assert peak<.98,'Unexpected clipping'
result=dict(samplerate=sr,baseline_rms=baseline,peak=peak,voices=rows)
(root/'build/playback-metrics.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
print('PASS: full production patch plays all eight latches and MIDI notes 36–43 in desktop Live. Physical pad acquisition is a separate hardware check.')
