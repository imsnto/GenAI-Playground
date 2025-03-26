import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, html
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.enums import ParseMode

from groq import Groq


# Load environment variables
load_dotenv()
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
groq_api_key = os.getenv('GROQ_API_KEY')


class Chat:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
    
    def clear_messages(self):
        self.messages = []

# Initialize Dispatcher
dp = Dispatcher()
client = Groq(api_key=groq_api_key)
chat = Chat()

def ask_groq(question: str) -> str:
    chat.add_message('user', question)

    # Call Groq API
    response =  client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=chat.messages
    )
    
    answer = response.choices[0].message.content
    chat.add_message('assistant', answer)
    return answer

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm GroqBot. I can help you query data from the Groq API.\nSend me your query.")

@dp.message(Command('ask'))
async def query(message: types.Message):
    question = message.text.split(' ', maxsplit=1)[1]
    answer = ask_groq(question)
    await message.reply(answer)

@dp.message(Command('clear'))
async def clear_chat(message: types.Message):
    chat.clear_messages()
    await message.reply("Chat cleared.")

async def main() -> None:
    bot = Bot(token=telegram_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())