import soundfile as sf

from sound_util.detect_sound import detect_sound_intervals, create_sound_file

try:
    sound_intervals = detect_sound_intervals(file_path="audio.wav")
    create_sound_file(sound_intervals)
except Exception as e:
    print(e)
    import glob
    import os

    file_list = glob.glob("sound_intervals_*.wav")
    for file_name in file_list:
        os.remove(file_name)
