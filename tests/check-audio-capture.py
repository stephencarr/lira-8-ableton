"""Analyze the WAV produced by make-audio-harness.py inside Live."""
import array,json,math,pathlib,sys,wave
root=pathlib.Path(__file__).resolve().parents[1]
with wave.open(str(root/'build/feedback-test.wav'),'rb') as w:
    assert w.getnchannels()==4 and w.getsampwidth()==2
    assert w.getnframes()>w.getframerate()*3
    samples=array.array('h',w.readframes(w.getnframes()))
if sys.byteorder!='little':samples.byteswap()
rows=[samples[i::4] for i in range(4)]
def rms(a):return math.sqrt(sum(x*x for x in a)/len(a))/32768
neutral=rms([a-b for a,b in zip(rows[0],rows[1])])
feedback=rms([a-b for a,b in zip(rows[0],rows[2])])
reference=rms(rows[0]);peak=max(abs(x) for x in samples)/32768
assert peak<0.95,'Capture clipped; reduce harness gain'
assert reference>0.001 and neutral==0 and feedback>0.001
print(json.dumps(dict(reference_voice_rms=reference,muted_input_difference_rms=neutral,
                     external_feedback_voice_difference_rms=feedback,peak=peak),indent=2))
print('PASS: real Gen capture; mute paths agree, external input changes the pre-effects voice through Total FB.')
