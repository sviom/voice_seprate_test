import librosa
import numpy as np
import matplotlib.pyplot as plt


def detect_sound_intervals(file_path, interval_duration=0.05, threshold=0.02):
    # Load the audio file
    y, sr = librosa.load(file_path)

    # plt.plot(y, label="data", alpha=0.7)
    # plt.grid()
    # plt.legend()
    # plt.show()

    # Calculate the number of samples in each interval
    interval_samples = int(interval_duration * sr)

    # Initialize the list to store results
    sound_intervals = []

    # Iterate over the signal in intervals
    for start in range(0, len(y), interval_samples):
        end = start + interval_samples

        # Get the current interval segment
        segment = y[start:end]

        # Calculate the root mean square (RMS) energy of the segment
        rms = np.sqrt(np.mean(segment**2))
        print("rms : ", rms)

        # Determine if the segment contains sound based on the threshold
        if rms >= threshold:
            sound_intervals.append((start / sr, end / sr))

    return sound_intervals


detect_sound_intervals(file_path="audio.wav")
# for interval in sound_intervals:
#     print(f"Sound detected from {interval[0]:.2f} to {interval[1]:.2f} seconds")
