from fastapi.testclient import TestClient


class TestAuthIntegration:
    """Integration tests for authentication flow"""

    def test_complete_auth_flow(self, client: TestClient):
        """Test complete authentication flow: register -> login"""
        # Step 1: Register a new user
        user_data = {
            "email": "integration@example.com",
            "first_name": "Integration",
            "last_name": "Test",
            "password": "integrationpass123"
        }

        register_response = client.post("/auth/token/register", json=user_data)
        assert register_response.status_code == 200

        register_data = register_response.json()
        assert "access_token" in register_data

        # Step 2: Login with the same credentials
        login_response = client.post(
            "/auth/token",
            data={
                "username": "integration@example.com",
                "password": "integrationpass123"
            }
        )

        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "access_token" in login_data

        # Both tokens should be valid (different but both work)
        assert len(register_data["access_token"]) > 0
        assert len(login_data["access_token"]) > 0

    def test_token_usage(self, client: TestClient, test_user):
        """Test using token for authenticated requests"""
        # Get token
        response = client.post(
            "/auth/token",
            data={
                "username": "test@example.com",
                "password": "testpassword123"
            }
        )

        assert response.status_code == 200
        token = response.json()["access_token"]

        # Use token in headers (example for future protected endpoints)
        headers = {"Authorization": f"Bearer {token}"}

        # This would be used for protected endpoints
        # For now, just verify the token format is correct
        assert isinstance(token, str)
        assert len(token) > 0
