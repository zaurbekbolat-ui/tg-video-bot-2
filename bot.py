import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TELEGRAM_BOT_TOKEN = "8522172198:AAGNiYBdw_-IIERKpfg432s0uewEk52FhUI"
HF_TOKEN = "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"

API_URL = "https://api-inference.huggingface.co/models/damo-vilab/text-to-video-ms-1.7b"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("👋 Привет! Напиши мне текстовый запрос на английском (например: 'a cute dog running on grass'), и я сгенерирую видео.")

@dp.message()
async def make_video(message: types.Message):
    prompt_text = message.text
    status_msg = await message.answer("⏳ Создаю видео, это займёт около 1-2 минут...")

    try:
        async with aiohttp.ClientSession() as session:
            payload = {"inputs": prompt_text}
            async with session.post(API_URL, headers=HEADERS, json=payload, timeout=aiohttp.ClientTimeout(total=180)) as resp:
                if resp.status == 200:
                    video_bytes = await resp.read()
                    video_file = types.BufferedInputFile(video_bytes, filename="video.mp4")
                    await message.answer_video(video=video_file, caption=f"🎬 {prompt_text}")
                elif resp.status == 503:
                    await message.answer("Модель прогревается на сервере. Подожди 30 секунд и отправь запрос ещё раз.")
                else:
                    await message.answer(f"Ошибка API: {resp.status}")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")
    finally:
        await status_msg.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
