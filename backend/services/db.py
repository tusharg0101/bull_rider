import os
import aiosqlite
import json
from typing import Any, List

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'tutorial.db')

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS tutorial_audio (
                step_number INTEGER PRIMARY KEY,
                audio_file TEXT NOT NULL
            )
        ''')
        await db.commit()

async def store_audio(step_number: int, audio_file: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO tutorial_audio (step_number, audio_file) VALUES (?, ?)",
            (step_number, audio_file)
        )
        await db.commit()

async def get_audio(step_number: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT audio_file FROM tutorial_audio WHERE step_number = ?",
            (step_number,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

async def get_total_steps():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM tutorial_audio") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def clear_audio():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM tutorial_audio")
        await db.commit()

async def init_name_address():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS name_address (
                address TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        await db.commit()
        

async def set_name_address(name: str, address: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO name_address (address, name) VALUES (?, ?)",
            (address, name)
        )
        await db.commit()

async def get_address_from_name(name: str) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT address FROM name_address WHERE name = ?",
            (name,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

async def delete_name_address(name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM name_address WHERE name = ?", (name,))
        await db.commit()

async def clear_name_address():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM name_address")
        await db.commit()
