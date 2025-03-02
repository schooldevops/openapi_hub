# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from api_hub.apis.project_members_api_base import BaseProjectMembersApi
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
from api_hub.models.project_member import ProjectMember


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/project_members",
    responses={
        200: {"model": List[ProjectMember], "description": "List of project members"},
        404: {"description": "Project members not found"},
    },
    tags=["Project Members"],
    summary="Get all project members",
    response_model_by_alias=True,
)
async def project_members_get(
) -> List[ProjectMember]:
    if not BaseProjectMembersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectMembersApi.subclasses[0]().project_members_get()


@router.post(
    "/project_members",
    responses={
        201: {"model": ProjectMember, "description": "Project member added successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["Project Members"],
    summary="Add new project member",
    response_model_by_alias=True,
)
async def project_members_post(
    project_member: ProjectMember = Body(None, description=""),
) -> ProjectMember:
    if not BaseProjectMembersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectMembersApi.subclasses[0]().project_members_post(project_member)


@router.delete(
    "/project_members/{project_member_id}",
    responses={
        204: {"description": "Project member deleted successfully"},
        404: {"description": "Project member not found"},
    },
    tags=["Project Members"],
    summary="Delete project member",
    response_model_by_alias=True,
)
async def project_members_project_member_id_delete(
    project_member_id: Annotated[StrictInt, Field(description="The ID of the project member to delete")] = Path(..., description="The ID of the project member to delete"),
) -> None:
    if not BaseProjectMembersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectMembersApi.subclasses[0]().project_members_project_member_id_delete(project_member_id)


@router.get(
    "/project_members/{project_member_id}",
    responses={
        200: {"model": ProjectMember, "description": "Project member details"},
        404: {"description": "Project member not found"},
    },
    tags=["Project Members"],
    summary="Get project member by ID",
    response_model_by_alias=True,
)
async def project_members_project_member_id_get(
    project_member_id: Annotated[StrictInt, Field(description="The ID of the project member to retrieve")] = Path(..., description="The ID of the project member to retrieve"),
) -> ProjectMember:
    if not BaseProjectMembersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectMembersApi.subclasses[0]().project_members_project_member_id_get(project_member_id)


@router.put(
    "/project_members/{project_member_id}",
    responses={
        200: {"model": ProjectMember, "description": "Project member updated successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["Project Members"],
    summary="Update project member",
    response_model_by_alias=True,
)
async def project_members_project_member_id_put(
    project_member_id: Annotated[StrictInt, Field(description="The ID of the project member to update")] = Path(..., description="The ID of the project member to update"),
    project_member: ProjectMember = Body(None, description=""),
) -> ProjectMember:
    if not BaseProjectMembersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectMembersApi.subclasses[0]().project_members_project_member_id_put(project_member_id, project_member)
