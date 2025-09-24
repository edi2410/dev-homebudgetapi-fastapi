from sqlmodel import Session, select
from app.db import get_session
from app.models.auth import UserInDB



def test_get_session():
    """Test session generator"""
    session_gen = get_session()
    session = next(session_gen)

    assert isinstance(session, Session)

    # Clean up
    try:
        next(session_gen)
    except StopIteration:
        pass  # Expected behavior


def test_database_operations(session: Session):
    """Test basic database operations"""
    # Create a user
    user = UserInDB(
        email="dbtest@example.com",
        first_name="DB",
        last_name="Test",
        hashed_password="hashed123"
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Test that user was created
    assert user.id is not None
    assert user.email == "dbtest@example.com"

    # Test querying
    found_user = session.exec(
        select(UserInDB).where(UserInDB.email == "dbtest@example.com")
    ).first()

    assert found_user is not None
    assert found_user.email == "dbtest@example.com"

