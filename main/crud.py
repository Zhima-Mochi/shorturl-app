from logging import error
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
import models, schemas
import random
import aiohttp

select = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate_code(code_len: int = 6, candidates: str = select):
    res = [None]*code_len
    width = len(candidates)
    for i in range(code_len):
        res[i] = candidates[random.randint(0, width-1)]
    return ''.join(res)

def get_code(db:Session, longUrl:str):
    retrieved_code = db.query(models.LongToCode).with_entities(
            models.LongToCode.code).filter(models.LongToCode.orig_url == longUrl).first()
    if retrieved_code:
        return  {"code": retrieved_code[0], "status": True}
    return None

def create_code(db: Session, longUrl: str):
    """Encodes a URL to a shortened URL.
    """
    code = generate_code()
    generate_count = 0
    while generate_count < 10 and db.query(models.LongToCode).filter(models.LongToCode.code == code).first():
        code = generate_code()
        generate_count += 1
    if generate_count == 10:
        db.query(models.LongToCode).filter(
            models.LongToCode.code == code).update({"orig_url": longUrl})
    else:
        longUrlCode = models.LongToCode(code=code, orig_url=longUrl,
                                        created_time=None)
        db.add(longUrlCode)
    try:
        db.commit()
        db.refresh(longUrlCode)
        return {"code": code, "status": True}
    except:
        db.rollback()
        return {"status": False}


def get_longUrl(db: Session, code: str):
    """Decodes a shortened URL to its original URL.
    """
    retrieved_longUrl = db.query(models.LongToCode).with_entities(
        models.LongToCode.orig_url).filter(models.LongToCode.code == code).first()
    if retrieved_longUrl:
        print('Match:', retrieved_longUrl)
        return retrieved_longUrl[0]
    else:
        print('Has no match.')
        return '/'
