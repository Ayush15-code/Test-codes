import numpy as np
import scipy.signal as signal
import librosa
import matplotlib.pyplot as plt

# Parameters
MIC_DISTANCE = 0.2  # Distance between microphones in meters
SPEED_OF_SOUND = 343  # Speed of sound in m/s at room temperature

# Function to compute TDOA using cross-correlation
def compute_tdoa(left_audio, right_audio):
    # Perform cross-correlation between left and right audio signals
    corr = signal.correlate(left_audio, right_audio, mode='full')
    
    # Find the lag (time shift) corresponding to the peak of the cross-correlation
    lag = np.argmax(np.abs(corr)) - (len(right_audio) - 1)
    
    # Convert lag to time delay (in seconds)
    time_delay = lag / RATE
    return time_delay

# Function to compute the angle from TDOA
def compute_angle(tdoa, mic_distance, speed_of_sound):
    # Angle of arrival in radians (sin^-1 formula)
    angle = np.arcsin(speed_of_sound * tdoa / mic_distance)
    return np.degrees(angle)  # Convert radians to degrees

# Load stereo audio file
filename = 'C:/Users/abhay/Downloads/Delayed Beep.wav'  # Replace with your file path
audio, RATE = librosa.load(filename, sr=None, mono=False)  # Load audio as stereo

# Check if the audio file is stereo
if audio.ndim == 1:
    raise ValueError("Audio file must be stereo (2 channels).")

# Split stereo channels into left and right audio signals
left_audio = audio[0, :]
right_audio = audio[1, :]

# Compute TDOA using cross-correlation
tdoa = compute_tdoa(left_audio, right_audio)

# Compute the angle of arrival from the TDOA
if abs(tdoa) <= (MIC_DISTANCE / SPEED_OF_SOUND):  # Ensure angle is valid
    angle = compute_angle(tdoa, MIC_DISTANCE, SPEED_OF_SOUND)
    print(f"TDOA: {tdoa:.6f} seconds, Estimated Angle: {angle:.2f} degrees")
else:
    print("TDOA out of valid range")

# Optional: Plot the audio signals for visualization
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.title("Left Channel Audio Signal")
plt.plot(left_audio)
plt.subplot(2, 1, 2)
plt.title("Right Channel Audio Signal")
plt.plot(right_audio)
plt.tight_layout()
plt.show()