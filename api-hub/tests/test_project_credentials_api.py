# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Any, List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from api_hub.models.project_credential import ProjectCredential  # noqa: F401


def test_project_credentials_get(client: TestClient):
    """Test case for project_credentials_get

    Get all project credentials
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/project_credentials",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_project_credentials_post(client: TestClient):
    """Test case for project_credentials_post

    Create new project credential
    """
    project_credential = {"expires_at":"2023-01-01T00:00:00Z","project_id":1,"api_key":"example_api_key","created_at":"2022-01-01T00:00:00Z","id":1,"created_by":1,"api_secret":"example_api_secret"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/project_credentials",
    #    headers=headers,
    #    json=project_credential,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_project_credentials_project_credential_id_delete(client: TestClient):
    """Test case for project_credentials_project_credential_id_delete

    Delete project credential
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/project_credentials/{project_credential_id}".format(project_credential_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_project_credentials_project_credential_id_get(client: TestClient):
    """Test case for project_credentials_project_credential_id_get

    Get project credential by ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/project_credentials/{project_credential_id}".format(project_credential_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_project_credentials_project_credential_id_put(client: TestClient):
    """Test case for project_credentials_project_credential_id_put

    Update project credential
    """
    project_credential = {"expires_at":"2023-01-01T00:00:00Z","project_id":1,"api_key":"example_api_key","created_at":"2022-01-01T00:00:00Z","id":1,"created_by":1,"api_secret":"example_api_secret"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/project_credentials/{project_credential_id}".format(project_credential_id=56),
    #    headers=headers,
    #    json=project_credential,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

