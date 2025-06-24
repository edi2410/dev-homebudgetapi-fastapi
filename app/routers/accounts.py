from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.sql.functions import current_user
from sqlmodel import Session, select

from app.core.auth import oauth2_scheme, get_current_user
from app.db import get_session
from app.dependencies import verify_token
from app.models.accounts import Account, AccountCreate
from app.models.auth import User

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[Depends(verify_token)]
)


@router.get("/")
def read_all_user_accounts(session: Session = Depends(get_session),
                           current_user: User = Depends(get_current_user)):
    return session.exec(select(Account).where(Account.user_id == current_user.id)).all()


@router.post("/")
def create_new_account(
    account: AccountCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_account = Account(
        **account.model_dump(),
        user_id=current_user.id
    )
    session.add(new_account)
    session.commit()
    session.refresh(new_account)
    return new_account

