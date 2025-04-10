import sounddevice as sd
import numpy as np

# Replace these with your microphone indexes
mic1_index = 1   # First microphone
mic2_index = 2   # Second microphone

# Sampling parameters
sample_rate = 44100  # Hz
channels = 1         # Mono input
chunk = 1024         # Frames per buffer

# Callback function for both mics
def callback1(indata, frames, time, status):
    if status:
        print(f"Mic1 Status: {status}")
    print(f"Mic 1: {np.mean(indata)}")

def callback2(indata, frames, time, status):
    if status:
        print(f"Mic2 Status: {status}")
    print(f"Mic 2: {np.mean(indata)}")

# Open two separate streams
stream1 = sd.InputStream(device=mic1_index, channels=channels, samplerate=sample_rate, callback=callback1)
stream2 = sd.InputStream(device=mic2_index, channels=channels, samplerate=sample_rate, callback=callback2)

print("Recording... Press Ctrl+C to stop.")

try:
    with stream1, stream2:
        sd.sleep(10000)  # Record for 10 seconds
except KeyboardInterrupt:
    print("\nStopping...")
