from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field

class AccountBase(SQLModel):
    account_number: str = Field(..., max_length=20, unique=True)
    account_nickname: Optional[str] = Field(default=None, max_length=200)
    balance: Decimal = Field(default=0.00)

class Account(AccountBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="userindb.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountCreate):
    account_nickname: Optional[str] = None
    balance: Optional[Decimal] = None
    account_number: Optional[str] = None

class AccountsRead(AccountBase):
    user_id: int = Field(foreign_key="userindb.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    id: int
