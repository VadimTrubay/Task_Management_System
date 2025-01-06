import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestUserViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def create_user(self):
        def create_user(**kwargs):
            return get_user_model().objects.create_user(**kwargs)

        return create_user

    @pytest.fixture
    def create_authenticated_client(self, api_client, create_user):
        user = create_user(username="testuser", password="password")
        token = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
        return api_client

    def test_signup(self, api_client):
        url = "/api/v1/users/signup/"
        data = {
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "access_token" in response.data

    def test_login(self, api_client, create_user):
        user = create_user(username="testuser", password="password")
        url = "/api/v1/users/login/"
        data = {"username": "testuser", "password": "password"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data

    def test_user_detail(self, create_authenticated_client):
        url = "/api/v1/users/me/"
        response = create_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "testuser"

    def test_logout(self, create_authenticated_client):
        url = "/api/v1/users/logout/"
        response = create_authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Successfully logout"
