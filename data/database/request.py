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
                await self.cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                                          (member_id, member_name, 'None', 'None', 'None', 'None', 'None'))
        await self.db.commit()

    async def update_user_form(self, member_id: int, name: str, age: int, sex: str, about: str, photo: str):
        await self.cursor.execute(f"UPDATE users SET name = ? WHERE id = ?", (name, member_id,))
        await self.cursor.execute(f"UPDATE users SET age = ? WHERE id = ?", (age, member_id,))
        await self.cursor.execute(f"UPDATE users SET sex = ? WHERE id = ?", (sex, member_id,))
        await self.cursor.execute(f"UPDATE users SET about = ? WHERE id = ?", (about, member_id,))
        await self.cursor.execute(f"UPDATE users SET photo = ? WHERE id = ?", (photo, member_id,))
        await self.db.commit()

    async def get_user_form(self, member_id: int) -> bool:
        async with self.db.execute(f"SELECT name FROM users WHERE id = ?", (member_id,)) as cursor:
            user_name = await cursor.fetchone()
            if user_name[0] == 'None':
                return False
            return True

    async def user_form_list(self, member_id: int) -> list[str | int]:
        async with self.db.execute("SELECT * FROM users WHERE id = ?", (member_id,)) as cursor:
            rows = await cursor.fetchall()
        return rows[0]

    async def user_form_name(self, member_id: int) -> str:
        async with self.db.execute(f"SELECT name FROM users WHERE id = ?", (member_id,)) as cursor:
            user_name = await cursor.fetchone()
        return user_name[0]

    async def user_form_age(self, member_id: int) -> str:
        async with self.db.execute(f"SELECT age FROM users WHERE id = ?", (member_id,)) as cursor:
            user_age = await cursor.fetchone()
        return user_age[0]

    async def user_form_about(self, member_id: int) -> str:
        async with self.db.execute(f"SELECT about FROM users WHERE id = ?", (member_id,)) as cursor:
            user_about = await cursor.fetchone()
        return user_about[0]

    async def close_database(self):
        await self.cursor.close()
        await self.db.close()