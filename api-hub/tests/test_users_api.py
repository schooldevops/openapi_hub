# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Any, List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from api_hub.models.user import User  # noqa: F401


def test_users_get(client: TestClient):
    """Test case for users_get

    Get all users
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/users",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_users_post(client: TestClient):
    """Test case for users_post

    Create new user
    """
    user = {"full_name":"John Doe","created_at":"2022-01-01T00:00:00Z","id":1,"email":"user@example.com"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/users",
    #    headers=headers,
    #    json=user,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_users_user_id_delete(client: TestClient):
    """Test case for users_user_id_delete

    Delete user
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/users/{user_id}".format(user_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_users_user_id_get(client: TestClient):
    """Test case for users_user_id_get

    Get user by ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/users/{user_id}".format(user_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_users_user_id_put(client: TestClient):
    """Test case for users_user_id_put

    Update user
    """
    user = {"full_name":"John Doe","created_at":"2022-01-01T00:00:00Z","id":1,"email":"user@example.com"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/users/{user_id}".format(user_id=56),
    #    headers=headers,
    #    json=user,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

