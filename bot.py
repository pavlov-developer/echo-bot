import asyncio
import sys
import os

from aiohttp import web

from dotenv import load_dotenv
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Token not found! Make sure the .env file exists and contains BOT_TOKEN=your_token")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"🇷🇺: Привет, {message.from_user.first_name}! Я эхо-бот.\n"
        "Пришли что угодно — верну обратно.\n\n"
        f"🇬🇧: Hello, {message.from_user.first_name}! I am an echo bot.\n" 
        "Send me anything — I will send it back."
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🇷🇺: Это эхо-бот. Напиши что-нибудь.\n\n"
        "🇬🇧: This is an echo bot. Write something."
    )


@dp.message()
async def echo(message: Message):
    if message.text:
        await message.answer(message.text)


async def handle(request):
    return web.Response(text="Bot is running")


async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

    print("Bot is started and ready to work")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())