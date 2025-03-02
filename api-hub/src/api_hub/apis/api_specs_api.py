# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from api_hub.apis.api_specs_api_base import BaseAPISpecsApi
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
from api_hub.models.api_spec import APISpec


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/api_specs/{api_spec_id}",
    responses={
        204: {"description": "API specification deleted successfully"},
        404: {"description": "API specification not found"},
    },
    tags=["API Specs"],
    summary="Delete API specification",
    response_model_by_alias=True,
)
async def api_specs_api_spec_id_delete(
    api_spec_id: Annotated[StrictInt, Field(description="The ID of the API specification to delete")] = Path(..., description="The ID of the API specification to delete"),
) -> None:
    if not BaseAPISpecsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAPISpecsApi.subclasses[0]().api_specs_api_spec_id_delete(api_spec_id)


@router.get(
    "/api_specs/{api_spec_id}",
    responses={
        200: {"model": APISpec, "description": "API specification details"},
        404: {"description": "API specification not found"},
    },
    tags=["API Specs"],
    summary="Get API specification by ID",
    response_model_by_alias=True,
)
async def api_specs_api_spec_id_get(
    api_spec_id: Annotated[StrictInt, Field(description="The ID of the API specification to retrieve")] = Path(..., description="The ID of the API specification to retrieve"),
) -> APISpec:
    if not BaseAPISpecsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAPISpecsApi.subclasses[0]().api_specs_api_spec_id_get(api_spec_id)


@router.put(
    "/api_specs/{api_spec_id}",
    responses={
        200: {"model": APISpec, "description": "API specification updated successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["API Specs"],
    summary="Update API specification",
    response_model_by_alias=True,
)
async def api_specs_api_spec_id_put(
    api_spec_id: Annotated[StrictInt, Field(description="The ID of the API specification to update")] = Path(..., description="The ID of the API specification to update"),
    api_spec: APISpec = Body(None, description=""),
) -> APISpec:
    if not BaseAPISpecsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAPISpecsApi.subclasses[0]().api_specs_api_spec_id_put(api_spec_id, api_spec)


@router.get(
    "/api_specs",
    responses={
        200: {"model": List[APISpec], "description": "List of API specifications"},
        404: {"description": "API specifications not found"},
    },
    tags=["API Specs"],
    summary="Get all API specifications",
    response_model_by_alias=True,
)
async def api_specs_get(
) -> List[APISpec]:
    if not BaseAPISpecsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAPISpecsApi.subclasses[0]().api_specs_get()


@router.post(
    "/api_specs",
    responses={
        201: {"model": APISpec, "description": "API specification created successfully"},
        400: {"description": "Invalid input"},
    },
    tags=["API Specs"],
    summary="Create new API specification",
    response_model_by_alias=True,
)
async def api_specs_post(
    api_spec: APISpec = Body(None, description=""),
) -> APISpec:
    if not BaseAPISpecsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAPISpecsApi.subclasses[0]().api_specs_post(api_spec)
