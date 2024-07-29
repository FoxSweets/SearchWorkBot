import aiosqlite


async def create_database():
	async with aiosqlite.connect("data/database/database.db") as db:
		cursor = await db.cursor()

		query = """
		CREATE TABLE IF NOT EXISTS "users" (
			"id"	INTEGER,
			"username"	TEXT,
			"types"	TEXT,
			"name"	TEXT,
			"age"	INTEGER,
			"sex"	TEXT,
			"country"	TEXT,
			"city"	TEXT,
			"about"	TEXT,
			"photo"	TEXT
		);
		"""

		await cursor.executescript(query)
		await db.commit()