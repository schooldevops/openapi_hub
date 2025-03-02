# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from api_hub.apis.projects_api_base import BaseProjectsApi
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
from api_hub.models.project import Project


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/projects",
    responses={
        200: {"model": List[Project], "description": "List of projects"},
        404: {"description": "Projects not found"},
    },
    tags=["Projects"],
    summary="Get all projects",
    response_model_by_alias=True,
)
async def projects_get(
) -> List[Project]:
    if not BaseProjectsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectsApi.subclasses[0]().projects_get()


@router.post(
    "/projects",
    responses={
        201: {"model": Project, "description": "Project created successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["Projects"],
    summary="Create new project",
    response_model_by_alias=True,
)
async def projects_post(
    project: Project = Body(None, description=""),
) -> Project:
    if not BaseProjectsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectsApi.subclasses[0]().projects_post(project)


@router.delete(
    "/projects/{project_id}",
    responses={
        204: {"description": "Project deleted successfully"},
        404: {"description": "Project not found"},
    },
    tags=["Projects"],
    summary="Delete project",
    response_model_by_alias=True,
)
async def projects_project_id_delete(
    project_id: Annotated[StrictInt, Field(description="The ID of the project to delete")] = Path(..., description="The ID of the project to delete"),
) -> None:
    if not BaseProjectsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectsApi.subclasses[0]().projects_project_id_delete(project_id)


@router.get(
    "/projects/{project_id}",
    responses={
        200: {"model": Project, "description": "Project details"},
        404: {"description": "Project not found"},
    },
    tags=["Projects"],
    summary="Get project by ID",
    response_model_by_alias=True,
)
async def projects_project_id_get(
    project_id: Annotated[StrictInt, Field(description="The ID of the project to retrieve")] = Path(..., description="The ID of the project to retrieve"),
) -> Project:
    if not BaseProjectsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectsApi.subclasses[0]().projects_project_id_get(project_id)


@router.put(
    "/projects/{project_id}",
    responses={
        200: {"model": Project, "description": "Project updated successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["Projects"],
    summary="Update project",
    response_model_by_alias=True,
)
async def projects_project_id_put(
    project_id: Annotated[StrictInt, Field(description="The ID of the project to update")] = Path(..., description="The ID of the project to update"),
    project: Project = Body(None, description=""),
) -> Project:
    if not BaseProjectsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProjectsApi.subclasses[0]().projects_project_id_put(project_id, project)
