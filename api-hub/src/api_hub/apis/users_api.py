# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from api_hub.apis.users_api_base import BaseUsersApi
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
from api_hub.models.user import User


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/users",
    responses={
        200: {"model": List[User], "description": "List of users"},
        404: {"description": "Users not found"},
    },
    tags=["Users"],
    summary="Get all users",
    response_model_by_alias=True,
)
async def users_get(
) -> List[User]:
    if not BaseUsersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseUsersApi.subclasses[0]().users_get()


@router.post(
    "/users",
    responses={
        201: {"model": User, "description": "User created successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["Users"],
    summary="Create new user",
    response_model_by_alias=True,
)
async def users_post(
    user: User = Body(None, description=""),
) -> User:
    if not BaseUsersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseUsersApi.subclasses[0]().users_post(user)


@router.delete(
    "/users/{user_id}",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
    },
    tags=["Users"],
    summary="Delete user",
    response_model_by_alias=True,
)
async def users_user_id_delete(
    user_id: Annotated[StrictInt, Field(description="The ID of the user to delete")] = Path(..., description="The ID of the user to delete"),
) -> None:
    if not BaseUsersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseUsersApi.subclasses[0]().users_user_id_delete(user_id)


@router.get(
    "/users/{user_id}",
    responses={
        200: {"model": User, "description": "User details"},
        404: {"description": "User not found"},
    },
    tags=["Users"],
    summary="Get user by ID",
    response_model_by_alias=True,
)
async def users_user_id_get(
    user_id: Annotated[StrictInt, Field(description="The ID of the user to retrieve")] = Path(..., description="The ID of the user to retrieve"),
) -> User:
    if not BaseUsersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseUsersApi.subclasses[0]().users_user_id_get(user_id)


@router.put(
    "/users/{user_id}",
    responses={
        200: {"model": User, "description": "User updated successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["Users"],
    summary="Update user",
    response_model_by_alias=True,
)
async def users_user_id_put(
    user_id: Annotated[StrictInt, Field(description="The ID of the user to update")] = Path(..., description="The ID of the user to update"),
    user: User = Body(None, description=""),
) -> User:
    if not BaseUsersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseUsersApi.subclasses[0]().users_user_id_put(user_id, user)
