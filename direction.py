import numpy as np
from scipy.io import wavfile
from scipy.signal import correlate
import matplotlib.pyplot as plt
import math

# Constants
SPEED_OF_SOUND = 343.0       # m/s
MIC_DISTANCE = 0.27           # meters between microphones

# Load WAV files
fs1, mic1 = wavfile.read("d:/Vulcan/audio1.wav")  # ← Use your actual paths here
fs2, mic2 = wavfile.read("d:/Vulcan/audio2.wav")

# Ensure both files have the same sample rate
assert fs1 == fs2, "Sample rates do not match!"
fs = fs1

# Convert stereo to mono if needed
if mic1.ndim > 1:
    mic1 = mic1[:, 0]
if mic2.ndim > 1:
    mic2 = mic2[:, 0]

# Convert to float32 to avoid casting errors
mic1 = mic1.astype(np.float32)
mic2 = mic2.astype(np.float32)

# Trim to same length
min_len = min(len(mic1), len(mic2))
mic1 = mic1[:min_len]
mic2 = mic2[:min_len]

# Optional: Check similarity (debug)
if np.allclose(mic1, mic2):
    print("⚠️ Warning: mic1 and mic2 are nearly identical!")

# Estimate initial lag (to align recordings)
initial_corr = correlate(mic1, mic2, mode='full')
initial_lag = np.argmax(initial_corr) - (len(mic1) - 1)

# Trim both signals to remove this initial lag
if initial_lag > 0:
    mic1 = mic1[initial_lag:]
    mic2 = mic2[:len(mic1)]
elif initial_lag < 0:
    mic2 = mic2[-initial_lag:]
    mic1 = mic1[:len(mic2)]



# Cross-correlation
correlation = correlate(mic1, mic2, mode='full')
lag = np.argmax(correlation) - (len(mic1) - 1)

# Time difference of arrival (TDOA)
time_diff = lag / fs
max_time_diff = MIC_DISTANCE / SPEED_OF_SOUND

# Clamp or validate the time diff
if abs(time_diff) > max_time_diff:
    print("⚠️ TDOA exceeds physical limit. Check setup.")
    angle_deg = float('nan')
else:
    angle_rad = math.asin(time_diff * SPEED_OF_SOUND / MIC_DISTANCE)
    angle_deg = math.degrees(angle_rad)

# Results
print(f"Lag: {lag} samples")
print(f"Time difference: {time_diff:.6f} s")
print(f"Estimated angle: {angle_deg:.2f}°")

# Plot correlation
lags = np.arange(-len(mic1) + 1, len(mic2))
plt.figure(figsize=(10, 4))
plt.plot(lags / fs, correlation)
plt.title("Cross-Correlation Between Microphones")
plt.xlabel("Time Lag (seconds)")
plt.ylabel("Correlation")
plt.grid(True)
plt.tight_layout()
plt.show()
