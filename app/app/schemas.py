from typing import List, Optional
from pydantic import BaseModel


class OrigUrl(BaseModel):
    url: str

    class Config:
        orm_mode = True
