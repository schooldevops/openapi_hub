# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Any, List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from api_hub.models.api_spec import APISpec  # noqa: F401


def test_api_specs_api_spec_id_delete(client: TestClient):
    """Test case for api_specs_api_spec_id_delete

    Delete API specification
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/api_specs/{api_spec_id}".format(api_spec_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_specs_api_spec_id_get(client: TestClient):
    """Test case for api_specs_api_spec_id_get

    Get API specification by ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api_specs/{api_spec_id}".format(api_spec_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_specs_api_spec_id_put(client: TestClient):
    """Test case for api_specs_api_spec_id_put

    Update API specification
    """
    api_spec = {"is_archived":0,"project_id":1,"spec_content":{},"access_role":"admin","description":"This is an example API specification.","created_at":"2022-01-01T00:00:00Z","id":1,"title":"Example API Specification","version":"1.0.0","created_by":1}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/api_specs/{api_spec_id}".format(api_spec_id=56),
    #    headers=headers,
    #    json=api_spec,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_specs_get(client: TestClient):
    """Test case for api_specs_get

    Get all API specifications
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api_specs",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_specs_post(client: TestClient):
    """Test case for api_specs_post

    Create new API specification
    """
    api_spec = {"is_archived":0,"project_id":1,"spec_content":{},"access_role":"admin","description":"This is an example API specification.","created_at":"2022-01-01T00:00:00Z","id":1,"title":"Example API Specification","version":"1.0.0","created_by":1}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api_specs",
    #    headers=headers,
    #    json=api_spec,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

