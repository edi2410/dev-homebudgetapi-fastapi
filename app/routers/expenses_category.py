from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import verify_token
from app.models.expense_categories import ExpensesCategoryRead, ExpensesCategoryCreate, ExpensesCategory, \
    ExpensesCategoryUpdate

router = APIRouter(
    prefix="/expenses",
    tags=["expenses_categories"],
    dependencies=[Depends(verify_token)]
)


@router.get("/categories/", response_model=List[ExpensesCategoryRead])
def read_categories(session: Session = Depends(get_session)):
    return session.exec(select(ExpensesCategory)).all()


@router.post("/categories/", response_model=ExpensesCategoryRead)
def create_category(category: ExpensesCategoryCreate, session: Session = Depends(get_session)):
    db_category = ExpensesCategory.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.get("/categories/{category_id}", response_model=ExpensesCategoryRead)
def read_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(ExpensesCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/categories/{category_id}", response_model=ExpensesCategoryRead)
def update_category(category_id: int, data: ExpensesCategoryUpdate, session: Session = Depends(get_session)):
    category = session.get(ExpensesCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    data_dict = data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(category, key, value)

    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(ExpensesCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}
