from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup



start_router = Router()



class

@start_router.message(Command('start'))
async def start(message: types.Message):
    await message.answer('start')
