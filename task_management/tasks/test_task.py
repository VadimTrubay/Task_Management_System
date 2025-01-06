import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestTaskViews:
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
        return api_client, user

    @pytest.fixture
    def create_task(self, create_authenticated_client):
        client, user = create_authenticated_client
        task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            priority="low",
            status="new",
            user=user,
        )
        return task

    def test_task_list_create(self, create_authenticated_client):
        client, user = create_authenticated_client
        url = "/api/v1/tasks/"
        data = {
            "title": "New Task",
            "description": "Description for new task",
            "priority": "low",
            "status": "new",
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Task"
        assert response.data["status"] == "new"
        assert response.data["user"] == user.id

    # def test_task_list_retrieval(self, create_authenticated_client, create_task):
    #     client, user = create_authenticated_client
    #     url = "/api/v1/tasks/"
    #     response = client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data["results"]) > 0
    #     assert response.data["results"][0]["title"] == create_task.title
    #
    # def test_task_retrieve(self, create_authenticated_client, create_task):
    #     client, user = create_authenticated_client
    #     url = f"/api/v1/tasks/{create_task.id}/"
    #     response = client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data["title"] == create_task.title
    #     assert response.data["status"] == create_task.status
    #
    # def test_task_update(self, create_authenticated_client, create_task):
    #     client, user = create_authenticated_client
    #     url = f"/api/v1/tasks/{create_task.id}/"
    #     data = {
    #         "title": "Updated Task Title",
    #         "description": "Updated Description",
    #         "priority": 3,
    #         "status": "completed"
    #     }
    #     response = client.put(url, data, format="json")
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data["title"] == "Updated Task Title"
    #     assert response.data["status"] == "completed"
    #
    # def test_task_delete(self, create_authenticated_client, create_task):
    #     client, user = create_authenticated_client
    #     url = f"/api/v1/tasks/{create_task.id}/"
    #     response = client.delete(url)
    #     assert response.status_code == status.HTTP_204_NO_CONTENT
    #     assert not Task.objects.filter(id=create_task.id).exists()
    #
    # def test_task_list_filter_by_status(self, create_authenticated_client, create_task):
    #     client, user = create_authenticated_client
    #     url = "/api/v1/tasks/?status=open"
    #     response = client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data["results"]) > 0
    #     assert response.data["results"][0]["status"] == "open"
    #
    # def test_task_list_filter_by_priority(self, create_authenticated_client, create_task):
    #     client, user = create_authenticated_client
    #     url = "/api/v1/tasks/?priority=1"
    #     response = client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data["results"]) > 0
    #     assert response.data["results"][0]["priority"] == 1
    #
    # def test_task_list_ordering(self, create_authenticated_client, create_task):
    #     client, user = create_authenticated_client
    #     url = "/api/v1/tasks/?ordering=priority"
    #     response = client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data["results"][0]["priority"] <= response.data["results"][-1]["priority"]
