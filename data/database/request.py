import aiosqlite
import asyncio


class BotBD:
    def __init__(self) -> None:
        self.db = None
        self.cursor = None

    async def connect(self):
        self.db = await aiosqlite.connect('data/database/database.db')
        self.cursor = await self.db.cursor()

    async def create_user(self, member_id: int, member_name: str):
        async with self.db.execute(f"SELECT id FROM users WHERE id = ?", (member_id,)) as cursor:
            if await cursor.fetchone() is None:
                await self.cursor.execute(f"INSERT INTO users VALUES (?, ?)",
                                          (member_id, member_name))
        await self.db.commit()

    async def close_database(self):
        await self.cursor.close()
        await self.db.close()