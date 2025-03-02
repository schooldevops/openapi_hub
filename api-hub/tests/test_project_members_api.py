# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Any, List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from api_hub.models.project_member import ProjectMember  # noqa: F401


def test_project_members_get(client: TestClient):
    """Test case for project_members_get

    Get all project members
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/project_members",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_project_members_post(client: TestClient):
    """Test case for project_members_post

    Add new project member
    """
    project_member = {"project_id":1,"user_id":1,"member_role":"admin","created_at":"2022-01-01T00:00:00Z","id":1}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/project_members",
    #    headers=headers,
    #    json=project_member,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_project_members_project_member_id_delete(client: TestClient):
    """Test case for project_members_project_member_id_delete

    Delete project member
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/project_members/{project_member_id}".format(project_member_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_project_members_project_member_id_get(client: TestClient):
    """Test case for project_members_project_member_id_get

    Get project member by ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/project_members/{project_member_id}".format(project_member_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_project_members_project_member_id_put(client: TestClient):
    """Test case for project_members_project_member_id_put

    Update project member
    """
    project_member = {"project_id":1,"user_id":1,"member_role":"admin","created_at":"2022-01-01T00:00:00Z","id":1}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/project_members/{project_member_id}".format(project_member_id=56),
    #    headers=headers,
    #    json=project_member,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

