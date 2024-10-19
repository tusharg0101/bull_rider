import os
from dotenv import load_dotenv
import aiomysql
from typing import List

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

async def get_connection():
    return await aiomysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )

async def store_audio(step_number: int, audio_file: str):
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO tutorial_audio (step_number, audio_file) VALUES (%s, %s) ON DUPLICATE KEY UPDATE audio_file = VALUES(audio_file)",
                (step_number, audio_file)
            )
            await conn.commit()

async def get_audio(step_number: int):
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT audio_file FROM tutorial_audio WHERE step_number = %s",
                (step_number,)
            )
            result = await cur.fetchone()
            return result[0] if result else None

async def get_total_steps():
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT COUNT(*) FROM tutorial_audio")
            result = await cur.fetchone()
            return result[0] if result else 0

async def clear_audio():
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM tutorial_audio")
            await conn.commit()
