from dotenv import load_dotenv
from sound_util.detect_sound import detect_sound_intervals, create_sound_file
from sound_util.stt_sound import create_speech_to_text
from sound_util.tts_sound import create_text_to_speech_file, tts_models

try:
    load_dotenv()
    sound_intervals = detect_sound_intervals(file_path="audio.wav")
    sound_file_list = create_sound_file(sound_intervals)
    text_list = create_speech_to_text(sound_file_list)
    create_text_to_speech_file(text_list, tts_models["alloy"])
except Exception as e:
    print(e)
    import glob
    import os

    file_list = glob.glob("sound_intervals_*.wav")
    for file_name in file_list:
        os.remove(file_name)
