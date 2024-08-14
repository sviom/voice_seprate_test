import os
import uuid
import librosa
import soundfile as sf
import numpy as np
import speech_recognition as sppech_r
import matplotlib.pyplot as plt

y, sr = librosa.load("audio.wav")

# Set the silence threshold
silence_threshold = 0.005
# silence_threshold = 0.01


# Compute the RMS (Root Mean Square) energy
rms = librosa.feature.rms(y=y)
# times = librosa.times_like(rms)
# plt.plot(times, rms[0])
# plt.show()

# Empty lists to save the audio data for silent and non-silent parts
silent_data = []
not_silent_data = []
all_data = []

# Variables to save the state
is_silent = rms[0, 0] < silence_threshold
start = 0

sound_data = []
for i in range(rms.shape[1]):
    # Check it the current state matches the computed state
    # if is_silent == (rms[0, i] < silence_threshold):
    #     continue
    is_silent = rms[0, i] < silence_threshold
    # Save the appropriate audio data
    if is_silent:
        if len(sound_data) > 0:
            all_data.append(
                {
                    "start_time": start,
                    "end_time": i,
                    "data": sound_data,
                    "is_slient": False,
                }
            )
            sound_data = []
    else:
        sound_data.extend(y[start:i])

    # Update the state and the start position
    # is_silent = not is_silent
    start = i

# Last chunk
if is_silent:
    # all_data.append(
    #     {"start_time": start, "end_time": -1, "data": y[start:], "is_slient": True}
    # )
    print("test")
# silent_data.extend(y[start:])
else:
    all_data.append(
        {"start_time": start, "end_time": -1, "data": y[start:], "is_slient": False}
    )
# not_silent_data.extend(y[start:])


# Write out the silent and non-silent parts to disk
# sf.write("silent.wav", np.array(silent_data), sr)
# sf.write("not_silent.wav", np.array(not_silent_data), sr)


text_list = []
r = sppech_r.Recognizer()

try:
    for sound in all_data:
        if sound["is_slient"] == True:
            continue

        temp_id = str(uuid.uuid4())
        temp_file_path = f"{temp_id}.wav"
        sf.write(temp_file_path, np.array(sound["data"]), sr)
        temp_duration = librosa.get_duration(path=temp_file_path)
        if temp_duration < 0.5:
            continue
        kr_audio = sppech_r.AudioData(
            frame_data=sound["data"], sample_rate=sr, sample_width=4
        )
        audio_text = r.recognize_whisper_api(kr_audio, api_key="")
        text_list.append(audio_text)
        os.remove(temp_file_path)
except Exception as e:
    print(f"error : {e}")
finally:
    os.remove(temp_file_path)
