# LIRA-8 for Ableton Live and Push

An eight-voice drone synthesizer for Max for Live, with a Push 3 pad interface, plus a companion audio effect for processing other tracks through its dual modulated delay and distortion.

Based on [Miguel Moreno's LIRA-8](https://github.com/MikeMorenoAudio/LIRA-8), originally made in Pure Data. This is a Gen/Max port with additional performance controls, not an official SOMA or Ableton product. It aims to preserve the character and signal flow of the software LIRA-8; it is not a circuit-accurate model of the analog LYRA-8.

**Download and load**

- [LIRA-Push-Pads.amxd](dist/LIRA-Push-Pads.amxd): the instrument, currently pad edition alpha 10, with temporary note tuning and external audio input. Load on a MIDI track.
- [LIRA-Delay.amxd](dist/LIRA-Delay.amxd): the new audio effect. Load on an audio track, a return track, or after another instrument.
- Keep [License.txt](License.txt) with copies you redistribute. On a GitHub file page, use **Download raw file**, or download the whole repository as a ZIP.

The devices contain their Gen and JavaScript code. They do not require Pure Data, samples, third-party externals, Node.js, or adjacent source files to play. Desktop testing used Live 12 Suite 12.4.16 with its bundled Max 9. Push work targets Push 3 standalone software 2.4.16. Other versions have not been verified. Live Suite, or Live with Max for Live, is required on the computer.

To transfer to Push standalone, pair Push with Live on the same network, then copy the devices into Push's User Library through Live's browser. Alternatively, put them in a Set, use Collect All and Save, and transfer the project. See Ableton's [Push project-transfer guide](https://help.ableton.com/hc/en-us/articles/8863603744412-Projects-on-Push-3-standalone) and [Max for Live compatibility notes](https://help.ableton.com/hc/en-us/articles/8506527153308-Max-for-Live-Devices-on-Push-3-standalone).

**Play the instrument**

Each voice has its own tuning and latch. Modulation amount, sharpness, modulation source and envelope speed are shared by each pair. Pitch and Hold affect voices 1–4 or 5–8. Hold can keep a group sounding even when its individual latches are off. Hyper LFO, feedback routing, dual delay and distortion create the interactions between voices.

Click **Open instrument** for the grouped desktop panel. **PD saved patch** recalls the included Pure Data comparison preset while leaving Master unchanged. Controls generally use the original 0–127 scale. MIDI notes 36–43 (C1–G1 in Live's octave naming) trigger the eight voices; note pitch selects a voice, not a conventional chromatic keyboard note.

On Push, select LIRA, enable **Pad Control** on the Output bank, and press **Note**. Arm the track or use Monitor In for the playable pads. The intended layout, from top to bottom, is:

- Top row: dark and inactive. Page selection from this row is deliberately disabled after an earlier experiment caused a Push restart.
- Next five rows: eight voice-level columns. From highest to lowest: full, 75%, 50%, 25%, mute. These change output levels while leaving the oscillator FM connections intact.
- Second row from the bottom: voice latches. An unlatched voice has an unlit latch pad.
- Bottom row: momentary voice playing. Pressure raises pitch by up to two semitones and increases sharpness together. Horizontal pitch movement and slide are ignored. Pressure requires Live/Push to deliver pressure data.

Use Push's device-bank display controls to select **Voices 1–2, Voices 3–4, Voices 5–6, Voices 7–8, Hyper LFO, Delay, Output, Voice Mixer**. These are eight permanent banks. There is no Perform or Setup bank. The bank names identify the active section; the old Pad Page parameter is retained internally for compatibility and does not select banks.

**Tune chords using notes (alpha 10 prototype)**

Select LIRA on Push, enable Pad Control, and use Note mode. On a voice-pair bank, hold **Shift** while turning **Tune 1–8** to step through chromatic notes. The readout temporarily includes the note and octave, such as `C#2 75.79`. A `~` marks a starting pitch between notes. Pressing Shift alone changes only the display. Release it to keep the exact fractional tuning value and return to the normal numeric display and continuous tuning. Octaves follow Live: MIDI 36 is C1, MIDI 60 is C3; tuning uses A = 440 Hz.

Hold Shift and turn **Pitch 1–4 / 5–8** to transpose the group in semitone steps relative to its pitch when Shift was pressed. All four intervals are preserved. Individual Tune selection accounts for the current group Pitch setting. These are oscillator base notes; FM, vibrato and pressure can still move the sounding pitch. Values stop at the original knob limits.

The desktop instrument window also has a **Note tune** toggle for the same behavior without Push. Playback automation is passed through while its parameter reports active automation; PD preset recall is passed through unchanged. No extra parameter banks are added. Shift is observed, never grabbed, and the encoders keep their native mappings. The tuning mode resets when pad control releases the surface. The desktop toggle is independent and resets on device load.

A real desktop Live harness verified all eight snapped pitches, parameter-to-DSP agreement, temporary note labels, group intervals, and return to continuous tuning. Run `python3 tests/make-tuning-harness.py`, load `build/LIRA-Tuning-Test.amxd`, wait four seconds, then run `python3 tests/check-tuning-capture.py` to repeat it. This silent harness sends no audio to speakers. Physical Shift observation and display refresh still need confirmation on Push standalone; this is a test build.

**Feed external audio into the synth**

The instrument now accepts external audio inside its own signal path, before the shared delay and distortion. With Total FB enabled, that combined output can modulate the voices. This follows the EXT IN / TOTAL FB relationship described in [SOMA's LYRA-8 manual, pages 4 and 7](https://somasynths.com/wp-content/uploads/2020/11/LYRA-8_manual_Eng_V2_1.pdf#page=7).

Use the **Output** bank on Push, or the **External Audio** section at the bottom of the desktop instrument window:

- **Audio From:** Off, Input 1, Input 2, Input 1/2, or Track 1–64. Hardware inputs refer to the current host audio device; on Push standalone they are Push's inputs.
- **Audio In:** incoming level, starting at zero. Raise it to hear the external signal; 127 applies no additional input attenuation before the mono sum.
- **Audio Tap:** Pre FX, Post FX, or Post Mixer for a track source. This has no effect on hardware-input choices.

Track choices refer to current track positions, so check them after reordering tracks. The desktop panel shows the resolved source name. A missing or ambiguous source is muted. The choices and eight banks stay fixed; the device does not rebuild bank layouts or parameter ranges at runtime. Hold controls remain on the voice-pair banks.

To hear cross-modulation, select an audio source and raise Audio In, latch a voice, choose **LFO / FB** as its pair's Source, raise that pair's Mod, and enable **Total FB** on the Hyper LFO bank. External audio can then affect the voice through the existing output-feedback loop. Delay Source **Self**, with Mod 1/2 raised, also lets the incoming signal affect delay-time modulation. Input gain and source selection are saved with the Set. With Audio From Off or Audio In at zero, the new input contributes no audio; the previous synthesis expression is preserved.

**Process another track through LIRA Delay**

The companion effect remains available for ordinary inserts and sends. It is a separate effect instance; use the synth's input above when external audio should participate in that synth's own feedback network.

For a shared send effect:

1. Add **LIRA-Delay.amxd** to a return track.
2. Leave its delay **Mix at maximum (127)**; this is the default.
3. Turn up that return's Send knob on any source track.
4. Adjust Time 1/2, Feedback and modulation. Use the source track's send and the return fader to balance the effect.

For a dedicated effects track:

1. Create an audio track and load LIRA Delay.
2. Set that track's **Audio From** to the source track. Choose Post FX or Post Mixer as needed.
3. Set **Monitor to In** on the effects track.
4. Leave Mix at 127 for a wet parallel path. The source still contributes its own dry signal if it also routes to Main.

For an insert, simply put LIRA Delay after the source instrument or on the source audio track, and lower Mix to blend dry signal with the repeats. These use Live's standard [track and return routing](https://www.ableton.com/en/manual/routing-and-i-o/).

The effect has three Push banks: **Delay, Hyper LFO, Output**. Input at 127 is unity gain; reducing it stops new material entering the delay without immediately clearing existing repeats. Master sets output level. Delay Mix and distortion Mix are separate controls. Select LFO as the delay modulation source and raise Mod 1/2 to hear the Hyper LFO affect delay time. AND/OR is omitted because it only feeds voice FM in the original instrument.

Stereo input is averaged to mono, and the same mono output is sent to both channels, matching the LIRA signal path. Even at dry Mix, the signal still passes through the output saturation and any distortion blend; use Live's device bypass for an unprocessed stereo signal. The delay retains the original low-level noise excitation and can self-oscillate at high feedback. Start with a low listening level.

For a microphone on **Push Input 1**, use an audio track with **Ext. In → 1**, **Monitor In**, and LIRA Delay. A useful insert starting point is Input 127, Master 80, Delay Mix 64, Feedback 30 and Dist Mix 0. A directly connected dynamic mic generally needs the **High** input mode in Setup → Audio. Push does not supply phantom power; a mic requiring it needs external power. Use headphones for live mic monitoring. See Ableton's [Push microphone FAQ](https://help.ableton.com/hc/en-us/articles/8483166334748-Push-3-Technical-FAQ) and [audio-track instructions](https://www.ableton.com/en/push/manual/#recording-audio).

**Source and builds**

Python 3 builds the devices using only its standard library. Node.js is needed only for the controller tests. From the repository root:

```sh
make
make test
```

Without Make:

```sh
python3 src/build.py
python3 src/build-pads.py
python3 src/build-delay.py
python3 tests/check.py
python3 tests/check-pads.py
python3 tests/check-delay.py
node tests/test-pads.cjs
LIRA_ID_SIGN=-1 node tests/test-pads.cjs
node tests/test-expression.cjs
node tests/test-audio-input.cjs
LIRA_ID_SIGN=-1 node tests/test-audio-input.cjs
node tests/test-tuning.cjs
LIRA_ID_SIGN=-1 node tests/test-tuning.cjs
```

- `src/build.py`: base Gen synthesis and Max instrument generator.
- `src/ui.py`: compact strip, grouped desktop window and preset recall.
- `src/inline_filters.py`: expands high-pass filter state at its call sites.
- `src/build-pads.py`, `src/pads.js`, `src/expression.js`: fixed Push banks, pad ownership/LEDs, mixer, latches and pressure handling.
- `src/tuning.py`, `src/tuning.js`: reversible Shift note selection using the original voice tuning curves, plus desktop note mode.
- `src/audio_input.py`, `src/audio-input.js`: embedded native Live DeviceIO routing, fixed source selectors and input-status display.
- `src/build-delay.py`: extracts the instrument's generated Hyper LFO, delay and distortion code into a native Max audio effect using `plugin~` and `plugout~`.
- `tests/`: structural and mocked controller regression checks.
- `assets/pd-preset.txt`: the comparison patch used by the recall button.
- `vendor/LIRA-8/`: upstream Pure Data standalone source and original licence, for reference.
- `build/`: ignored base-instrument intermediate files.
- `dist/`: ready-to-load devices, editable Max patches, embedded Gen/controller source and instrument bank definitions.

Edit the generators, then rebuild; hand edits to `dist/` are overwritten. Builds are deterministic. A regression check removes only the new input declarations and summing expression, then compares the remaining DSP against the alpha 8 hash. The original Pure Data reference is included so the port can be inspected and improved. Differences include explicit 64-sample feedback boundaries and a rectangular RMS approximation of Pure Data's windowed detector; exact waveform matching is not claimed.

**Validation and current limits**

The automated checks cover AMXD containers, patch wiring, saved parameters, bank mappings, embedded code, preservation of the synthesis engine, signed Live API IDs, pad acquisition/release, latch handling, saved mixer levels, forced LED repaint, reconnects and pressure on all eight voices. Controller tests use a mocked Live API and cannot prove hardware stability.

LIRA Delay loaded successfully in desktop Live and received audio from a separate LIRA instrument track via Audio From / Post Mixer / Monitor In. With delay Mix at 127, its output rose from approximately −84 dBFS idle to −45 dBFS with a quiet source voice. The panel was visually checked. The owner also confirmed microphone audio with delay through Push Input 1 and headphones on standalone.

The integrated synth input was tested in desktop Live by routing another track through its native audio bus. A separate silent Gen harness records the oscillator before effects, comparing input gain zero, routing gate zero, and external audio with Total FB. To repeat this DSP test, run `python3 tests/make-audio-harness.py`, load the generated `build/LIRA-Feedback-Test.amxd` in Live, wait six seconds, then run `python3 tests/check-audio-capture.py`. The harness disables random delay noise and records at reduced level to make comparisons deterministic; it sends no audio to speakers. The new synth input still needs testing on Push standalone.

The instrument's pad takeover has worked on the owner's Push. Alpha 8's refreshed mixer LEDs and full bottom-row behavior still need confirmation on hardware. Top-row bank selection remains disabled, and no crash-associated bank-selection API call is shipped. This repository contains the current source and devices, not the withdrawn crashing experimental builds. Save your Set before trying a new build.

**Attribution**

Original LIRA-8 synthesis and Pure Data implementation: Miguel Moreno / [Mike Moreno DSP](https://github.com/MikeMorenoDSP). Pure Data: Miller Puckette and contributors. The original plugin distribution used Camomile by Pierre Guillot; this Max port does not require it. The original Standard Improved BSD licence is preserved in [License.txt](License.txt). This project is unaffiliated with SOMA Laboratory, Ableton or Cycling '74.
