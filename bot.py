import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from groq import AsyncGroq

TELEGRAM_BOT_TOKEN = "8522172198:AAGNiYBdw_-IIERKpfg432s0uewEk52FhUI"
GROQ_API_KEY = "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"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
client = AsyncGroq(api_key=GROQ_API_KEY)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("👋 Привет! Я твой личный ИИ-ассистент. Задавай любой вопрос на русском или любом другом языке — я на связи!")

@dp.message()
async def chat_ai(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Ты дружелюбный, эрудированный и полезный ИИ-помощник. Отвечай подробно, понятно и с форматированием."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        answer = response.choices[0].message.content
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
