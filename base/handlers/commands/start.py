from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from base import orm as db

start_router = Router()

class StartStatesGroup(StatesGroup):
    user_details = State()
    full_name_w8ing = State()
    ph_number_w8ing = State()
    contract = State()

@start_router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer(" Are you an existing customer?")
    await state.set_state(StartStatesGroup.user_details)

# User details VALIDATION
@start_router.message(StartStatesGroup.user_details)
async def start(message: types.Message, state: FSMContext):
    await state.update_data(user_details=message.text)
    if message.text == "yes" or message.text == "Yes":
        await message.answer("Send your contract number")
        await state.set_state(StartStatesGroup.contract)
    elif message.text == "no" or message.text == "No":
        await state.set_state(StartStatesGroup.full_name_w8ing)
        await message.answer("Send your full name please")
    else:
        await message.answer("Please enter Yes or No")
        await state.set_state(StartStatesGroup.user_details)

# Existing customer
@start_router.message(StartStatesGroup.contract)
async def save_name(message: types.Message, state: FSMContext):
    citizen_data = await db.get_citizen(message.text)
    if not citizen_data:
        await message.answer("Contract number was wrong")
        return
    if message.text.isdigit() and len(message.text) == 9:
        await state.update_data(contract=message.text)
        pass

    else:
        await message.answer("Please enter your contract number of 9 numbers")
        await state.set_state(StartStatesGroup.contract)
    ''' + ELIF with support technology'''


# New customer
@start_router.message(StartStatesGroup.full_name_w8ing)
async def save_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer('Отправите Срочно ваше номер...')
    await state.set_state(StartStatesGroup.ph_number_w8ing)
@start_router.message(StartStatesGroup.ph_number_w8ing)
async def save_number(message: types.Message, state: FSMContext):
    await state.update_data(full_number=message.text)
    # await get_data()


async def get_data(state: FSMContext, message: types.Message):
    data = await state.get_data()
    await message.answer(data['full_name']+data['ph_number'])
    # await state.clear()
