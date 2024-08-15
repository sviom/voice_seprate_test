def create_speech_to_text(audio_file_list: list[str]):
    import os
    from openai import OpenAI

    text_list = []
    open_ai_key = os.getenv("OPEN_AI_KEY")
    client = OpenAI(api_key=open_ai_key)
    for audio_file_path in audio_file_list:
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file
            )
            print(transcription.text)
            text_list.append(transcription.text)

    return text_list
