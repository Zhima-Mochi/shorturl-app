import asyncio
import sqlalchemy as sa

from aiomysql.sa import create_engine
from sqlalchemy import text

metadata = sa.MetaData()


async def go():
    engine = await create_engine(user='root', db='shorturl',
                                 host='127.0.0.1', password='password')
    async with engine.acquire() as conn:
        result = await conn.execute(text("SELECT * FROM long_to_code;"))
        print(result)
    engine.close()
    await engine.wait_closed()


asyncio.run(go())
