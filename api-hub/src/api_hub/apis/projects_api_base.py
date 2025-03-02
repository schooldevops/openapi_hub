# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import Any, List
from typing_extensions import Annotated
from api_hub.models.project import Project


class BaseProjectsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseProjectsApi.subclasses = BaseProjectsApi.subclasses + (cls,)
    async def projects_get(
        self,
    ) -> List[Project]:
        ...


    async def projects_post(
        self,
        project: Project,
    ) -> Project:
        ...


    async def projects_project_id_delete(
        self,
        project_id: Annotated[StrictInt, Field(description="The ID of the project to delete")],
    ) -> None:
        ...


    async def projects_project_id_get(
        self,
        project_id: Annotated[StrictInt, Field(description="The ID of the project to retrieve")],
    ) -> Project:
        ...


    async def projects_project_id_put(
        self,
        project_id: Annotated[StrictInt, Field(description="The ID of the project to update")],
        project: Project,
    ) -> Project:
        ...
