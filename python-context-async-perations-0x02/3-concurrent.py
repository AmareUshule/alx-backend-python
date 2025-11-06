"""Concurrent asynchronous database queries using aiosqlite"""

import asyncio
import aiosqlite

DB_NAME = "mydb.sqlite"

async def async_fetch_users():
    """Fetch all users"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    """Fetch users older than 40"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """Run both queries concurrently"""
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:")
    for row in results_all:
        print(row)
    print("\nUsers older than 40:")
    for row in results_older:
        print(row)

# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

