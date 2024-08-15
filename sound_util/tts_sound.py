from typing import Literal, get_args

tts_models = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def create_text_to_speech_file(
    tts_text: list[str], model_name: get_args(tts_models), is_hd_audio: bool = False
):
    """
    Open AI API 를 이용하여 TTS 서비스 이용하기

    :param tts_text: 변환하고자 하는 텍스트
    :param model_name: 원하는 모델
    :param is_hd_audio: 고음질 모드 선택 여부

    """
    import os
    import uuid
    from openai import OpenAI

    try:

        for text in tts_text:
            file_path = os.path.join(f"{str(uuid.uuid4())}.mp3")
            open_ai_key = os.getenv("OPEN_AI_KEY")

            client = OpenAI(api_key=open_ai_key)
            response = client.audio.speech.create(
                model="tts-1-hd" if is_hd_audio else "tts-1",
                voice=model_name,
                input=text,
            )

            response.write_to_file(file_path)
        # return file_path
    except Exception as e:
        from main import logger
        from datetime import datetime

        logger.info(
            "[create_text_to_speech_file] "
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        logger.error(f"[create_text_to_speech_file]  error : {format(e)}")
        return ""
