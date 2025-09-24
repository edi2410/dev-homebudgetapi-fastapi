from datetime import timedelta
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.auth import UserInDB, UserCreate, Token
from app.core.auth import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
)


class TestPasswordHashing:
    """Test password hashing functions"""

    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False


class TestAuthentication:
    """Test authentication functions"""

    def test_authenticate_user_success(self, session: Session, test_user: UserInDB):
        """Test successful user authentication"""
        user = authenticate_user(session, "test@example.com", "testpassword123")

        assert user is not None
        assert user.email == "test@example.com"

    def test_authenticate_user_wrong_email(self, session: Session, test_user: UserInDB):
        """Test authentication with wrong email"""
        user = authenticate_user(session, "wrong@example.com", "testpassword123")
        assert user is False

    def test_authenticate_user_wrong_password(self, session: Session, test_user: UserInDB):
        """Test authentication with wrong password"""
        user = authenticate_user(session, "test@example.com", "wrongpassword")
        assert user is False


class TestAccessToken:
    """Test access token creation and validation"""

    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiration(self):
        """Test access token creation with custom expiration"""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)

        assert isinstance(token, str)
        assert len(token) > 0


class TestAuthEndpoints:
    """Test authentication endpoints"""

    def test_login_success(self, client: TestClient, test_user: UserInDB):
        """Test successful login"""
        response = client.post(
            "/auth/token",
            data={
                "username": "test@example.com",
                "password": "testpassword123"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_wrong_credentials(self, client: TestClient, test_user: UserInDB):
        """Test login with wrong credentials"""
        response = client.post(
            "/auth/token",
            data={
                "username": "test@example.com",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Incorrect email or password"

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with nonexistent user"""
        response = client.post(
            "/auth/token",
            data={
                "username": "nonexistent@example.com",
                "password": "somepassword"
            }
        )

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Incorrect email or password"

    def test_register_success(self, client: TestClient):
        """Test successful user registration"""
        user_data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpassword123"
        }

        response = client.post("/auth/token/register", json=user_data)

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_register_duplicate_email(self, client: TestClient, test_user: UserInDB):
        """Test registration with duplicate email"""
        user_data = {
            "email": "test@example.com",  # Already exists
            "first_name": "Another",
            "last_name": "User",
            "password": "anotherpassword123"
        }

        response = client.post("/auth/token/register", json=user_data)

        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Email already registered"

    def test_register_invalid_data(self, client: TestClient):
        """Test registration with invalid data"""
        # Missing required fields
        user_data = {
            "email": "incomplete@example.com",
            "first_name": "Incomplete"
            # Missing last_name and password
        }

        response = client.post("/auth/token/register", json=user_data)
        assert response.status_code == 422  # Validation error

    def test_register_invalid_email(self, client: TestClient):
        """Test registration with invalid email format"""
        user_data = {
            "email": "invalid-email",
            "first_name": "Invalid",
            "last_name": "Email",
            "password": "password123"
        }

        response = client.post("/auth/token/register", json=user_data)
        assert response.status_code == 422  # Validation error


class TestAuthModels:
    """Test authentication models"""

    def test_user_create_model(self):
        """Test UserCreate model"""
        user_data = {
            "email": "model@example.com",
            "first_name": "Model",
            "last_name": "Test",
            "password": "modelpassword123"
        }

        user = UserCreate(**user_data)

        assert user.email == "model@example.com"
        assert user.first_name == "Model"
        assert user.last_name == "Test"
        assert user.password == "modelpassword123"

    def test_user_in_db_model(self, session: Session):
        """Test UserInDB model"""
        user = UserInDB(
            email="indb@example.com",
            first_name="InDB",
            last_name="Test",
            hashed_password="hashed123"
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.id is not None
        assert user.email == "indb@example.com"
        assert user.first_name == "InDB"
        assert user.last_name == "Test"
        assert user.hashed_password == "hashed123"

    def test_token_model(self):
        """Test Token model"""
        token = Token(
            access_token="sample_token_string",
            token_type="bearer"
        )

        assert token.access_token == "sample_token_string"
        assert token.token_type == "bearer"

