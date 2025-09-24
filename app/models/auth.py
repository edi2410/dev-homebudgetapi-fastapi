from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    email: EmailStr | None = None

class User(SQLModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None

class UserCreate(User):
    password: str

class UserInDB(User, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str