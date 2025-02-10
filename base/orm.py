import sqlite3

from config import DB_PATH, PHOTOS_PATH



async def connect_to_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

async def get_citizen(citizen_contract:str):
    '''gets citizen by his contract number.'''
    conn, cursor = await connect_to_db()
    citizen_data = cursor.execute(
        f'''SELECT id, name_lastname, date_of_birth, phone_number telegram_id
        FROM citizen_data WHERE contract == "{citizen_contract}"''').fetchone()
    conn.close()
    return citizen_data

async def save_photo(citizen_contract:str,photo_name:str):
    conn, cursor = await connect_to_db()
    citizen = await get_citizen(citizen_contract)
    citizen_id = citizen[0]
    photo_path = PHOTOS_PATH + '/' + photo_name
    cursor.execute(
        f'''INSERT INTO bills
        (citizen_id, photo, cost) VALUES("{citizen_id}","{photo_path}","1")'''
    )
    conn.commit()
    conn.close()

# import asyncio
# asyncio.run(save_photo('1234567890','AgACAgIAAxkBAAP0Z64Iigi_caDFrjXZukm6eEaGBlMAAvrwMRvxlXFJQofe9WehcBoBAAMCAAN5AAM2BA.jpg'))
#
