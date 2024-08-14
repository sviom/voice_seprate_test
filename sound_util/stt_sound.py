def create_speech_to_text():
    import os
    import speech_recognition as sr

    open_ai_key = os.getenv("OPEN_AI_KEY")

    r = sr.Recognizer()

    r.recognize_whisper_api(api_key=open_ai_key)

    print("test")
