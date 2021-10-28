from db import session
from model import LongToCode
import aiohttp
import random


async def valid_url(url):
    try:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.get(url) as resp:
                return resp.status == 200
    except:
        return False


class LongUrlCode:
    select = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, session=session):
        self.session = session

    def getcode(self):
        res = []
        width = len(self.select)
        for i in range(6):
            res.append(self.select[random.randint(0, width-1)])
        return ''.join(res)

    def encode(self, longUrl: str):
        """Encodes a URL to a shortened URL.
        """
        retrieved_code = self.session.query(LongToCode).with_entities(
            LongToCode.code).filter(LongToCode.orig_url == longUrl).all()
        if retrieved_code:
            return retrieved_code[0][0]
        else:
            code = self.getcode()
            generate_count = 0
            while(generate_count < 10 and self.session.query(LongToCode).filter(LongToCode.code == code).all()):
                code = self.getcode()
                generate_count += 1
            if generate_count == 10:
                self.session.query(LongToCode).filter(
                    LongToCode.code == code).update({"orig_url": longUrl})
            else:
                obj = LongToCode(code=code, orig_url=longUrl,
                                 created_time=None)
                self.session.add(obj)
            self.session.commit()
            return code

    def decode(self, code: str):
        """Decodes a shortened URL to its original URL.
        """
        retrieved_longUrl = self.session.query(LongToCode).with_entities(
            LongToCode.orig_url).filter(LongToCode.code == code).all()
        if retrieved_longUrl:
            print('Match:', retrieved_longUrl[0])
            return retrieved_longUrl[0][0]
        else:
            print('Has no match.')
            return '/'
