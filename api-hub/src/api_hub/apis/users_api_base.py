# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import Any, List
from typing_extensions import Annotated
from api_hub.models.user import User


class BaseUsersApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseUsersApi.subclasses = BaseUsersApi.subclasses + (cls,)
    async def users_get(
        self,
    ) -> List[User]:
        ...


    async def users_post(
        self,
        user: User,
    ) -> User:
        ...


    async def users_user_id_delete(
        self,
        user_id: Annotated[StrictInt, Field(description="The ID of the user to delete")],
    ) -> None:
        ...


    async def users_user_id_get(
        self,
        user_id: Annotated[StrictInt, Field(description="The ID of the user to retrieve")],
    ) -> User:
        ...


    async def users_user_id_put(
        self,
        user_id: Annotated[StrictInt, Field(description="The ID of the user to update")],
        user: User,
    ) -> User:
        ...
