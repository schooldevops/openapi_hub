# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import Any, List
from typing_extensions import Annotated
from api_hub.models.api_spec import APISpec


class BaseAPISpecsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAPISpecsApi.subclasses = BaseAPISpecsApi.subclasses + (cls,)
    async def api_specs_api_spec_id_delete(
        self,
        api_spec_id: Annotated[StrictInt, Field(description="The ID of the API specification to delete")],
    ) -> None:
        ...


    async def api_specs_api_spec_id_get(
        self,
        api_spec_id: Annotated[StrictInt, Field(description="The ID of the API specification to retrieve")],
    ) -> APISpec:
        ...


    async def api_specs_api_spec_id_put(
        self,
        api_spec_id: Annotated[StrictInt, Field(description="The ID of the API specification to update")],
        api_spec: APISpec,
    ) -> APISpec:
        ...


    async def api_specs_get(
        self,
    ) -> List[APISpec]:
        ...


    async def api_specs_post(
        self,
        api_spec: APISpec,
    ) -> APISpec:
        ...
