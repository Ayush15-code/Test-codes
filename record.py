import pyaudio
import numpy as np
import wave
# standard parameters
chunk = 1024
rate = 44100
channels = 1
record_seconds = 10  # Duration of recording in seconds
# output_filename = "combined_audio.wav"
output_filename1 = "audio1.wav"
output_filename2 = "audio2.wav"

# Device index for mics
mic1_index = 1
mic2_index = 3

p = pyaudio.PyAudio()

# Open input streams for both microphones
# Save audio data in 16-bit integer format
stream1 = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=mic1_index, frames_per_buffer=chunk)
stream2 = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=mic2_index, frames_per_buffer=chunk)

# Open output WAV file 
wf1 = wave.open(output_filename1, "wb")
wf1.setnchannels(channels)
wf1.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf1.setframerate(rate)

wf2 = wave.open(output_filename2, "wb")
wf2.setnchannels(channels)
wf2.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf2.setframerate(rate)

print("Recording...")

try:
    for _ in range(0, int(rate / chunk * record_seconds)):  # Record for a set duration
        data1 = np.frombuffer(stream1.read(chunk), dtype=np.int16)
        data2 = np.frombuffer(stream2.read(chunk), dtype=np.int16)
        
        # combined_data = np.clip(data1.astype(np.int32) + data2.astype(np.int32), -32768, 32767).astype(np.int16)

        wf1.writeframes(data1.tobytes())
        wf2.writeframes(data2.tobytes())


        print(f"Mic 1: {np.mean(data1)} | Mic 2: {np.mean(data2)}")

except KeyboardInterrupt:
    print("\nStopping")

# Stop and close streams
stream1.stop_stream()
stream1.close()
stream2.stop_stream()
stream2.close()
p.terminate()
wf1.close()
wf2.close()
# wf.close()


# print(f"Recording saved as {output_filename}")


# The above code records audio from two microphones simultaneously, combines the audio data, and saves it to a WAV file.
# It uses the PyAudio library to handle audio input and output, and NumPy for numerical operations on the audio data.   
