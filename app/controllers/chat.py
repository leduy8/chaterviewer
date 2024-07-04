from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse

from app.services.chat import get_chat_response, text_to_speech, transcribe_audio

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def talk(file: UploadFile):
    user_message = transcribe_audio(file)
    chat_response = get_chat_response(user_message)
    text_to_speech(chat_response)

    def iterfile():
        with open("output.mp3", mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
