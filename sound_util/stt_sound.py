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


def stt_using_google(audio_file_path: str, lang_text: str = "ko-KR"):
    import speech_recognition as sr

    text = ""
    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio = r.record(source)  # read the entire audio file

        response = r.recognize_google_cloud(
            audio_data=audio,
            credentials_json="anai-dub-2d8d74989129.json",
            language=lang_text,
        )
        print("successful: ", response)
        text = response
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")

    except sr.RequestError as e:
        print(
            "Could not request results from Google Cloud Speech service; {0}".format(e)
        )

    return text
