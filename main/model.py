from sqlalchemy import Column, Integer, String, DateTime
import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class LongToCode(Base):
    __tablename__ = 'long_to_code'
    code = Column(String(6), primary_key=True)
    orig_url = Column(String(500), unique=True)
    created_time = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, code, orig_url, created_time):
        self.code = code
        self.orig_url = orig_url
        self.created_time = created_time
