from typing import Optional
from src.db import ServerType, Server
from .marzneshin import MarzneshinClient, MarzneshinAdmin


class ClinetManager:
    @classmethod
    async def generate_access_token(
        self, *, config: dict[str, str], server_type: ServerType
    ) -> Optional[str]:
        match server_type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(config["host"])
                token = await api.generate_access_token(
                    username=config["username"], password=config["password"]
                )
                token = token.access_token if token and token.is_sudo else None
            case _:
                return

        return token

    @classmethod
    async def get_admin(
        self, *, username: str, access: str, server: Server
    ) -> Optional[MarzneshinAdmin]:
        match server.type:
            case ServerType.MARZNESHIN:
                api = MarzneshinClient(server.config["host"])
                admin = await api.get_admin(username=username, access=access)
            case _:
                return

        return admin

    @classmethod
    def get_configs(self):
        pass

    @classmethod
    def get_user(self):
        pass

    @classmethod
    def get_users(self):
        pass

    @classmethod
    def create_user(self):
        pass

    @classmethod
    def update_user(self):
        pass

    @classmethod
    def remove_user(self):
        pass
