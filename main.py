import librosa
import numpy as np
import soundfile as sf


def detect_sound_intervals(file_path, interval_duration=0.05, threshold=0.002):
    # Load the audio file
    y, sr = librosa.load(file_path)

    # Calculate the number of samples in each interval
    interval_samples = int(interval_duration * sr)

    # Initialize the list to store results
    sound_intervals = []
    no_slient_data = []

    is_slient = True
    start_sec = 0
    end_sec = 0

    for start in range(0, len(y), interval_samples):
        end = start + interval_samples

        if is_slient:
            start_sec += interval_duration
        end_sec += interval_duration

        # Get the current interval segment
        segment = y[start:end]

        # Calculate the root mean square (RMS) energy of the segment
        rms = np.sqrt(np.mean(segment**2))

        # Determine if the segment contains sound based on the threshold
        if rms >= threshold:
            no_slient_data.extend(segment)
            is_slient = False
        else:
            if len(no_slient_data) > 0 and not is_slient:
                sound_intervals.append(
                    {
                        "start_time": start_sec,
                        "end_time": end_sec,
                        "segment": no_slient_data,
                        "sr": sr,
                    }
                )
                no_slient_data = []
                is_slient = True

    return sound_intervals


try:
    sound_intervals = detect_sound_intervals(file_path="audio.wav")
    for interval in sound_intervals:
        start_sec = float(interval["start_time"])
        end_sec = float(interval["end_time"])
        segment = interval["segment"]
        sr = interval["sr"]

        if (end_sec - start_sec) >= 1:
            sf.write(
                f"sound_intervals_{str(start_sec)}.wav", data=segment, samplerate=sr
            )
            print(f"Sound detected from {start_sec:.2f} to {end_sec:.2f} seconds")

except Exception as e:
    print(e)
finally:
    import glob
    import os

    file_list = glob.glob("sound_intervals_*.wav")
    for file_name in file_list:
        os.remove(file_name)
