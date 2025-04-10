import numpy as np
import scipy.signal as signal
import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
MIC_DISTANCE = 0.27  # Distance between microphones in meters
SPEED_OF_SOUND = 343  # Speed of sound in m/s at room temperature
CHUNK_SIZE = 1024  # Number of samples per chunk (adjust based on latency needs)

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
filename1 = 'd:/Vulcan/PL.wav'  # Replace with your file path
left_audio, RATE = librosa.load(filename1, sr=None, mono=True)  # Load audio as mono
# Load stereo audio file
filename2 = 'd:/Vulcan/AR.wav'  # Replace with your file path
right_audio, RATE = librosa.load(filename2, sr=None, mono=True)  # Load audio as mono


# Set up the figure for plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
ax1.set_title("Left Channel Audio Signal")
ax2.set_title("Right Channel Audio Signal")
line_left, = ax1.plot([], [], lw=2)
line_right, = ax2.plot([], [], lw=2)

# Initialize the plot limits
ax1.set_xlim(0, CHUNK_SIZE)
ax2.set_xlim(0, CHUNK_SIZE)
ax1.set_ylim(-1, 1)
ax2.set_ylim(-1, 1)

# Text box to display angle
angle_text = ax2.text(0.5, 0.9, "Angle: 0.00 degrees", transform=ax2.transAxes, fontsize=12, ha='center')

# Initialize the plot
def init():
    line_left.set_data([], [])
    line_right.set_data([], [])
    angle_text.set_text("Angle: 0.00 degrees")
    return line_left, line_right, angle_text

# Function to update the plot and calculate angle for each chunk
def update(frame):
    start = frame * CHUNK_SIZE
    end = start + CHUNK_SIZE
    left_chunk = left_audio[start:end]
    right_chunk = right_audio[start:end]

    # Compute TDOA using cross-correlation
    tdoa = compute_tdoa(left_chunk, right_chunk)
    
    # Compute the angle of arrival from the TDOA
    if abs(tdoa) <= (MIC_DISTANCE / SPEED_OF_SOUND):  # Ensure angle is valid
        angle = compute_angle(tdoa, MIC_DISTANCE, SPEED_OF_SOUND)
    else:
        angle = 0.0  # Invalid angle, set to 0
    
    # Update the plot lines
    line_left.set_data(np.arange(len(left_chunk)), left_chunk)
    line_right.set_data(np.arange(len(right_chunk)), right_chunk)

    # Update the angle display
    angle_text.set_text(f"Angle: {angle:.2f} degrees")
    if angle > 0:
        print("Right")
    elif angle < 0:
        print("Left")
    return line_left, line_right, angle_text

# Number of frames to process
num_frames = len(left_audio) // CHUNK_SIZE

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, interval=50)

# Show the plot
plt.tight_layout()
plt.show()
