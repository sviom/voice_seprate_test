def create_speech_to_text(audio_file_list: list[str]):
    import os
    import speech_recognition as sr
    from speech_recognition import AudioData

    open_ai_key = os.getenv("OPEN_AI_KEY")

    from openai import OpenAI

    client = OpenAI(api_key=open_ai_key)

    for audio_file_path in audio_file_list:
        with open(audio_file_path, "rb") as audio_file:
            # audio_file = open(audio_file_path, "rb")
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file
            )
            print(transcription.text)

    print("test")
