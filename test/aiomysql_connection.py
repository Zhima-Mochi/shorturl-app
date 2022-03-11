import asyncio
import aiomysql


async def test_example():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='password',
                                      db='shorturl')
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM long_to_code;")
            print(cur.description)
            # (r,) = await cur.fetchone()
    pool.close()
    await pool.wait_closed()


asyncio.run(test_example())
