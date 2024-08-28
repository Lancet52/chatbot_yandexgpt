import requests, os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router_handler = Router()


@router_handler.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать!')


@router_handler.message(F.text)
async def texttobot(message: Message):
    prompt = {
        "modelUri": f"gpt://{os.getenv('FOLDER')}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "500"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты брутальный робот пылесос"
            },
            {
                "role": "user",
                "text": message.text
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {os.getenv('AITOKEN')}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()['result']['alternatives'][0]['message']['text']
    await message.answer(result)
