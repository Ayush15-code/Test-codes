import pyaudio
import numpy as np

chunk = 1024
rate = 44100
channels = 1

# Device index for mics
mic1_index = 1
mic2_index = 2 

# Create PyAudio streams
p = pyaudio.PyAudio()

stream1 = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=mic1_index, frames_per_buffer=chunk)
stream2 = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=mic2_index, frames_per_buffer=chunk)

print("Recording")

try:
    while True:
        data1 = np.frombuffer(stream1.read(chunk), dtype=np.int16)
        data2 = np.frombuffer(stream2.read(chunk), dtype=np.int16)

        print(f"Mic 1: {np.mean(data1)} | Mic 2: {np.mean(data2)}")

except KeyboardInterrupt:
    print("\nStopping")
    stream1.stop_stream()
    stream1.close()
    stream2.stop_stream()
    stream2.close()
    p.terminate()

