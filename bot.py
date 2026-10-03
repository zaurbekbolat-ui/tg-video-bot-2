import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TELEGRAM_BOT_TOKEN = "8522172198:AAGNiYBdw_-IIERKpfg432s0uewEk52FhUI"
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("👋 Привет! Я твой личный ИИ-ассистент. Задавай любой вопрос — я готов помочь!")

@dp.message()
async def chat_ai(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Ты дружелюбный, эрудированный и полезный ИИ-помощник. Отвечай подробно, понятно и грамотно на русском языке."},
            {"role": "user", "content": message.text}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GROQ_URL, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    answer = data["choices"][0]["message"]["content"]
                    await message.answer(answer)
                else:
                    err_text = await resp.text()
                    await message.answer(f"⚠️️ Ошибка API ({resp.status}): {err_text[:200]}")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка соединения: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
