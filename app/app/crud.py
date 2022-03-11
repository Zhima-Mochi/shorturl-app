from sqlalchemy.ext.asyncio import AsyncSession
import models
import random
from sqlalchemy.future import select

select_code = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


async def generate_code(code_len: int = 6, candidates: str = select_code):
    res = [None]*code_len
    width = len(candidates)
    for i in range(code_len):
        res[i] = candidates[random.randint(0, width-1)]
    return ''.join(res)


async def get_code(session: AsyncSession, longUrl: str):
    result = await session.execute(select(models.LongToCode.code).where(models.LongToCode.orig_url == longUrl))
    retrieved_code = result.first()
    if retrieved_code:
        return {"code": retrieved_code[0], "status": True}
    return None


async def create_code(session: AsyncSession, longUrl: str):
    """Encodes a URL to a shortened URL.
    """
    code = await generate_code()
    generate_count = 0
    while generate_count < 10 and (await session.execute(select(models.LongToCode).where(models.LongToCode.code == code))).first():
        code = generate_code()
        generate_count += 1
    if generate_count == 10:
        await session.execute(select(models.LongToCode).where(
            models.LongToCode.code == code).values({"orig_url": longUrl}))
    else:
        longUrlCode = models.LongToCode(code=code, orig_url=longUrl,
                                        created_time=None)
        session.add(longUrlCode)
    try:
        await session.commit()
        await session.refresh(longUrlCode)
        return {"code": code, "status": True}
    except:
        await session.rollback()
        return {"status": False}


async def get_longUrl(session: AsyncSession, code: str):
    """Decodes a shortened URL to its original URL.
    """
    result = await session.execute(select(models.LongToCode.orig_url).where(models.LongToCode.code == code))
    retrieved_longUrl = result.first()
    if retrieved_longUrl:
        print('Match:', retrieved_longUrl)
        return retrieved_longUrl[0]
    else:
        print('Has no match.')
        return '/'
