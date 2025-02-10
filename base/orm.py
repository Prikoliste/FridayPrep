import sqlite3
from config import DB_PATH



async def connect_to_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

async def get_citizen(citizen_contract:str):
    #gets citizen by his contract number.
    conn, cursor = await connect_to_db()
    citizen_data = cursor.execute(
        f'''SELECT id, name_lastname, date_of_birth, phone_number telegram_id
        FROM citizen_data WHERE contract == "{citizen_contract}"''').fetchone()
    conn.close()
    return citizen_data
