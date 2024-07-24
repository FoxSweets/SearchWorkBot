import aiosqlite


async def create_database():
	async with aiosqlite.connect("data/database/database.db") as db:
		cursor = await db.cursor()

		query = """
		CREATE TABLE IF NOT EXISTS "users" (
			"id"	INTEGER,
			"username"	TEXT
		);
		"""

		await cursor.executescript(query)
		await db.commit()