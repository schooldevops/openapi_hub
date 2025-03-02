# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import Any, List
from typing_extensions import Annotated
from api_hub.models.project_member import ProjectMember


class BaseProjectMembersApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseProjectMembersApi.subclasses = BaseProjectMembersApi.subclasses + (cls,)
    async def project_members_get(
        self,
    ) -> List[ProjectMember]:
        ...


    async def project_members_post(
        self,
        project_member: ProjectMember,
    ) -> ProjectMember:
        ...


    async def project_members_project_member_id_delete(
        self,
        project_member_id: Annotated[StrictInt, Field(description="The ID of the project member to delete")],
    ) -> None:
        ...


    async def project_members_project_member_id_get(
        self,
        project_member_id: Annotated[StrictInt, Field(description="The ID of the project member to retrieve")],
    ) -> ProjectMember:
        ...


    async def project_members_project_member_id_put(
        self,
        project_member_id: Annotated[StrictInt, Field(description="The ID of the project member to update")],
        project_member: ProjectMember,
    ) -> ProjectMember:
        ...
