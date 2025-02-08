
PHOTOS_PATH = 'files/photos/'
import sqlite3

# conn = sqlite3.connect('test.db')
# c = conn.cursor()

# c.execute('CREATE TABLE User(id INTEGER PRIMARY KEY, ph_number TEXT, name TEXT, chat_id INTEGER)')
# c.execute('CREATE TABLE Photos(id INTEGER PRIMARY KEY, user_id INTEGER, photo_path TEXT)')

# c.execute('INSERT INTO User(ph_number, name) VALUES (?, ?)', ('+3565496850', 'Misha'))
# conn.commit()


# data = c.execute('SELECT id, ph_number, name FROM User WHERE id = ?', (1,)).fetchone()


# table_id, ph_number, name = data



from aiogram import Dispatcher, Bot, types, F
import asyncio

bot = Bot('7885759081:AAHm-uj3zUYYrrKGvKewNKIuWtRDl3N5i1g')
dp = Dispatcher()


@dp.message(F.photo)
async def photo_handler(message: types.Message):
    # print(message.from_user.id)
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = PHOTOS_PATH + photo.file_id + '.jpg'
    await bot.download_file(file.file_path, file_path)
    user_table_id = await get_user_id_by_tg_id(message.from_user.id)
    await save_file_to_db(user_table_id, file_path)

async def save_file_to_db(user_table_id: int, file_path: str):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO Photos(user_id, photo_path) VALUES (?, ?)", (user_table_id, file_path))
    conn.commit()
    conn.close()

async def get_user_id_by_tg_id(tg_id: int):
    conn = sqlite3.connect('friday_data.db')
    c = conn.cursor()
    data = c.execute('SELECT id  FROM User WHERE chat_id = ?', (tg_id,)).fetchone()
    conn.close()
    if data:
        return data[0]
    else:
        return None



asyncio.run(dp.start_polling(bot))