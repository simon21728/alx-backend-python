import asyncio
import aiosqlite

DB_PATH = 'my_database.db'  # Replace with your database path

# --- Asynchronous function to fetch all users ---
async def async_fetch_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

# --- Asynchronous function to fetch users older than 40 ---
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            return older_users

# --- Run both queries concurrently ---
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    all_users, users_over_40 = results
    print("All users:", all_users)
    print("Users older than 40:", users_over_40)

# --- Execute the async fetch ---
asyncio.run(fetch_concurrently())
