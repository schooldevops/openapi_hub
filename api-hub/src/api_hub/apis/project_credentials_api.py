# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from api_hub.apis.project_credentials_api_base import BaseProjectCredentialsApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from api_hub.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictInt
from typing import Any, List
from typing_extensions import Annotated
from api_hub.models.project_credential import ProjectCredential


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/project_credentials",
    responses={
        200: {"model": List[ProjectCredential], "description": "List of project credentials"},
        404: {"description": "Project credentials not found"},
    },
    tags=["Project Credentials"],
    summary="Get all project credentials",
    response_model_by_alias=True,
)
async def project_credentials_get(
) -> List[ProjectCredential]:
    if not BaseProjectCredentialsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectCredentialsApi.subclasses[0]().project_credentials_get()


@router.post(
    "/project_credentials",
    responses={
        201: {"model": ProjectCredential, "description": "Project credential created successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["Project Credentials"],
    summary="Create new project credential",
    response_model_by_alias=True,
)
async def project_credentials_post(
    project_credential: ProjectCredential = Body(None, description=""),
) -> ProjectCredential:
    if not BaseProjectCredentialsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectCredentialsApi.subclasses[0]().project_credentials_post(project_credential)


@router.delete(
    "/project_credentials/{project_credential_id}",
    responses={
        204: {"description": "Project credential deleted successfully"},
        404: {"description": "Project credential not found"},
    },
    tags=["Project Credentials"],
    summary="Delete project credential",
    response_model_by_alias=True,
)
async def project_credentials_project_credential_id_delete(
    project_credential_id: Annotated[StrictInt, Field(description="The ID of the project credential to delete")] = Path(..., description="The ID of the project credential to delete"),
) -> None:
    if not BaseProjectCredentialsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectCredentialsApi.subclasses[0]().project_credentials_project_credential_id_delete(project_credential_id)


@router.get(
    "/project_credentials/{project_credential_id}",
    responses={
        200: {"model": ProjectCredential, "description": "Project credential details"},
        404: {"description": "Project credential not found"},
    },
    tags=["Project Credentials"],
    summary="Get project credential by ID",
    response_model_by_alias=True,
)
async def project_credentials_project_credential_id_get(
    project_credential_id: Annotated[StrictInt, Field(description="The ID of the project credential to retrieve")] = Path(..., description="The ID of the project credential to retrieve"),
) -> ProjectCredential:
    if not BaseProjectCredentialsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectCredentialsApi.subclasses[0]().project_credentials_project_credential_id_get(project_credential_id)


@router.put(
    "/project_credentials/{project_credential_id}",
    responses={
        200: {"model": ProjectCredential, "description": "Project credential updated successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["Project Credentials"],
    summary="Update project credential",
    response_model_by_alias=True,
)
async def project_credentials_project_credential_id_put(
    project_credential_id: Annotated[StrictInt, Field(description="The ID of the project credential to update")] = Path(..., description="The ID of the project credential to update"),
    project_credential: ProjectCredential = Body(None, description=""),
) -> ProjectCredential:
    if not BaseProjectCredentialsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectCredentialsApi.subclasses[0]().project_credentials_project_credential_id_put(project_credential_id, project_credential)
