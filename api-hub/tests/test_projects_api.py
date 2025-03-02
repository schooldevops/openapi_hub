# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Any, List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from api_hub.models.project import Project  # noqa: F401


def test_projects_get(client: TestClient):
    """Test case for projects_get

    Get all projects
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/projects",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_projects_post(client: TestClient):
    """Test case for projects_post

    Create new project
    """
    project = {"is_archived":0,"name":"Example Project","description":"This is an example project.","created_at":"2022-01-01T00:00:00Z","id":1,"created_by":1}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/projects",
    #    headers=headers,
    #    json=project,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_projects_project_id_delete(client: TestClient):
    """Test case for projects_project_id_delete

    Delete project
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/projects/{project_id}".format(project_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_projects_project_id_get(client: TestClient):
    """Test case for projects_project_id_get

    Get project by ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/projects/{project_id}".format(project_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_projects_project_id_put(client: TestClient):
    """Test case for projects_project_id_put

    Update project
    """
    project = {"is_archived":0,"name":"Example Project","description":"This is an example project.","created_at":"2022-01-01T00:00:00Z","id":1,"created_by":1}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/projects/{project_id}".format(project_id=56),
    #    headers=headers,
    #    json=project,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

