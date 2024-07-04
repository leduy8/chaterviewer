import json
import os

import requests
from openai import OpenAI, RateLimitError

from app.config import config

client = OpenAI(api_key=config.OPENAI_KEY, organization=config.OPENAI_ORG)
assets_path = "app/assets/"


def transcribe_audio(file):
    try:
        # Save the blob first
        with open(assets_path + file.filename, "wb") as buffer:
            buffer.write(file.file.read())

        # audio_file= open(assets_path + file.filename, "rb")
        # transcription = client.audio.transcriptions.create(
        #   model="whisper-1",
        #   file=audio_file
        # )
        # print(transcription.text)
        # return transcription.text
        transcription = "Hello Scott"
        return transcription
    except RateLimitError:
        return {"message": "You have exceeded your quota"}


def get_chat_response(user_message):
    # Load message and append user message
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})

    # Send to chatGPT
    # gpt_response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=messages
    # )
    # parsed_gpt_response = gpt_response.choices[0].message.content
    parsed_gpt_response = "Hello Liam"

    # Save messages
    save_messages(user_message=user_message, gpt_response=parsed_gpt_response)

    return parsed_gpt_response


def load_messages():
    messages = []
    file = assets_path + "database.json"

    # if file is empty, we add system context (system role)
    # if file is not empty, loop histo ry and load context to messages

    empty = os.stat(file).st_size == 0

    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            [messages.append(item) for item in data]
    else:
        messages.append({"role": "system", "content": config.STARTING_CONTEXT})

    return messages


def save_messages(user_message, gpt_response):
    file = assets_path + "database.json"
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response})
    with open(file, "w") as f:
        json.dump(messages, f)


def text_to_speech(text):
    try:
        CHUNK_SIZE = 1024
        voice_id = "iP95p4xoKVk53GoZ742B"  # Chris's AI voice
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"  # noqa: E231
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
        }
        headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": config.ELEVENLABS_KEY}

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(assets_path + "output.mp3", "wb") as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            return response.content
        else:
            print("Something is wrong")
            print(response.status_code)
            print(response.content)

    except Exception as e:
        print(e)
