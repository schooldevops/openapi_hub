# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import Any, List
from typing_extensions import Annotated
from api_hub.models.project_credential import ProjectCredential


class BaseProjectCredentialsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseProjectCredentialsApi.subclasses = BaseProjectCredentialsApi.subclasses + (cls,)
    async def project_credentials_get(
        self,
    ) -> List[ProjectCredential]:
        ...


    async def project_credentials_post(
        self,
        project_credential: ProjectCredential,
    ) -> ProjectCredential:
        ...


    async def project_credentials_project_credential_id_delete(
        self,
        project_credential_id: Annotated[StrictInt, Field(description="The ID of the project credential to delete")],
    ) -> None:
        ...


    async def project_credentials_project_credential_id_get(
        self,
        project_credential_id: Annotated[StrictInt, Field(description="The ID of the project credential to retrieve")],
    ) -> ProjectCredential:
        ...


    async def project_credentials_project_credential_id_put(
        self,
        project_credential_id: Annotated[StrictInt, Field(description="The ID of the project credential to update")],
        project_credential: ProjectCredential,
    ) -> ProjectCredential:
        ...
