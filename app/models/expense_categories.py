from typing import Optional
from sqlmodel import SQLModel, Field


class ExpensesCategoryBase(SQLModel):
    name: str
    description: Optional[str] = None


class ExpensesCategoryCreate(ExpensesCategoryBase):
    pass


class ExpensesCategoryRead(ExpensesCategoryBase):
    id: int

class ExpensesCategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ExpensesCategory(ExpensesCategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
