from dotenv import load_dotenv
from sound_util.detect_sound import detect_sound_intervals, create_sound_file
from sound_util.stt_sound import create_speech_to_text, stt_using_google
from sound_util.tts_sound import create_text_to_speech_file, tts_models

try:
    load_dotenv()
    stt_using_google(audio_file_path="audio.wav")

    sound_intervals = detect_sound_intervals(file_path="audio.wav")

    import os
    import uuid

    temp_guid = str(uuid.uuid4())
    temp_path = os.path.join("temp", temp_guid)

    sound_file_list = create_sound_file(
        sound_intervals=sound_intervals, write_file_path=temp_path
    )
    text_list = create_speech_to_text(sound_file_list)
    create_text_to_speech_file(text_list, tts_models["alloy"])
except Exception as e:
    print(e)
    import glob
    import os

    file_list = glob.glob("sound_intervals_*.wav")
    for file_name in file_list:
        os.remove(file_name)
