from aiogram import Dispatcher, Bot, types, F
import asyncio
from config import TOKEN
from base.routing import main_router

bot = Bot(TOKEN)
dp = Dispatcher()


async def starter():
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print(1)
    asyncio.run(starter())
