from typing import Optional
from ..core import ClientBase, RequestCore
from ._types import MarzneshinAdmin, MarzneshinToken


class MarzneshinClient(ClientBase, RequestCore):
    def __init__(self, host: str):
        super().__init__(host)

    async def generate_access_token(
        self, username: str, password: str
    ) -> Optional[MarzneshinToken]:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        return await self.post(
            endpoint="/api/admins/token",
            data=data,
            response_model=MarzneshinToken,
        )

    async def get_admin(self, username: str, access: str) -> Optional[MarzneshinAdmin]:
        return await self.get(
            endpoint=f"/api/admins/{username}",
            access=access,
            response_model=MarzneshinAdmin,
        )

    def get_configs(self):
        pass

    def get_user(self):
        pass

    def get_users(self):
        pass

    def create_user(self):
        pass

    def update_user(self):
        pass

    def remove_user(self):
        pass
