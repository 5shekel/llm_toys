import streamlit as st
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import tempfile

def generate_sine_wave(frequency, amplitude, phase, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def combine_oscillators(oscillators, duration, sample_rate):
    combined_wave = np.zeros(int(sample_rate * duration))
    for osc in oscillators:
        wave = generate_sine_wave(
            osc['frequency'], 
            osc['amplitude'], 
            osc['phase'], 
            duration, 
            sample_rate
        )
        combined_wave += wave
    return combined_wave



st.title('Multi-Oscillator App with Phase and Playback')
st.write('a quick attempt by an LLM to make an https://noisio.de/boards/levitation-oscillator')
st.image('https://i.imgur.com/UBwVcOo.jpeg', width=300)

# Default parameters
duration = 5  # 5 seconds
sample_rate = 44100

# Sliders for four oscillators
oscillators = []
for i in range(1, 5):
    st.subheader(f'Oscillator {i}')
    frequency = st.slider(f'Frequency {i} (Hz)', 100.0, 2000.0, 440.0)
    amplitude = st.slider(f'Amplitude {i}', 0.1, 1.0, 0.2)
    phase = st.slider(f'Phase {i} (Radians)', 0.0, 2*np.pi, 0.0)
    oscillators.append({"frequency": frequency, "amplitude": amplitude, "phase": phase})

# Generate and plot the combined wave
combined_wave = combine_oscillators(oscillators, duration, sample_rate)
st.line_chart(combined_wave[:5000])

# Convert the wave to 16-bit PCM WAV format
combined_wave_16bit = np.int16(combined_wave / np.max(np.abs(combined_wave)) * 32767)

# Streamlit audio player
"hit play to plyback the combined wave"
st.audio(combined_wave_16bit, format='audio/wav', sample_rate=sample_rate, )

# Play the combined wave continuously
def play_audio(wave, sample_rate):
    wave = np.int16(wave / np.max(np.abs(wave)) * 32767)
    audio_segment = AudioSegment(
        wave.tobytes(), 
        frame_rate=sample_rate,
        sample_width=2,  # 16-bit PCM
        channels=1
    )
    play(audio_segment)

"the live play doesn't work on streamlit sharing, but it does work locally"
if st.checkbox('Play Audio Continuously'):
        play_audio(combined_wave, sample_rate)
else:
    st.stop()

st.write('source https://github.com/5shekel/llm_toys')
