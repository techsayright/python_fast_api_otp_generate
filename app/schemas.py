from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserCreate_resp(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # id : Optional[str] = None
    id: str