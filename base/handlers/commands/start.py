from email.charset import add_alias
import easyocr
from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from base import orm as db
from config import *
start_router = Router()

class StartStatesGroup(StatesGroup):
    user_details = State()
    contract = State()
    photo = State()
    # full_name_w8ing = State()
    # ph_number_w8ing = State()

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
        await message.answer("Sorry you are not in the list.\n Please email us or come to our office")
        # await state.set_state(StartStatesGroup.full_name_w8ing)
        # await message.answer("Send your full name please")
    else:
        await message.answer("Please enter Yes or No")
        await state.set_state(StartStatesGroup.user_details)

# Existing customer
@start_router.message(StartStatesGroup.contract)
async def check_contract(message: types.Message, state: FSMContext):
    citizen_data = await db.get_citizen(message.text)
    if not citizen_data:
        await message.answer("Contract number is wrong")
        await state.set_state(StartStatesGroup.contract)
        return
    else:
        await state.update_data(contract=message.text)
        await state.set_state(StartStatesGroup.photo)
        await message.answer("Photo.")


@start_router.message(StartStatesGroup.photo)
async def save_photo(message: types.Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1]
        photo_name =  photo.file_id + '.jpg'
        file_path = PHOTOS_PATH + '/' + photo_name

        file = await message.bot.get_file(photo.file_id)
        await message.bot.download_file(file.file_path, file_path)

        data = await state.get_data()

        ### ТУТ МНЕ БЫЛО ЛЕНЬ ПИСАТЬ АЛГОРИТМ ДЛЯ ПОДСЧЕТА
        await state.update_data(file_path = file_path)
        cost = await analyze_photo(state,message)
        await db.save_photo(data.get("contract"), photo_name, cost * 0.9)

        await message.answer("Photo saved")

    else:
        await message.answer("Photo not saved")


async def analyze_photo(state: FSMContext, message: types.Message):
    data = await state.get_data()
    file_path = data["file_path"]
    reader = easyocr.Reader(['en'])  # this needs to run only once to load the model into memory
    result = reader.readtext(file_path, detail=False, allowlist='0123456789', width_ths=1, height_ths=0.1, rotation_info=[90, 180 ,270])
    result = result[0]
    result = int(result.replace(" ", ""))

    await message.answer(f'{result}')
    return result

# # New customer
# @start_router.message(StartStatesGroup.full_name_w8ing)
# async def save_name(message: types.Message, state: FSMContext):
#     await state.update_data(full_name=message.text)
#     await message.answer('Отправите Срочно ваше номер...')
#     await state.set_state(StartStatesGroup.ph_number_w8ing)
# @start_router.message(StartStatesGroup.ph_number_w8ing)
# async def save_number(message: types.Message, state: FSMContext):
#     await state.update_data(full_number=message.text)
#     # await get_data()



