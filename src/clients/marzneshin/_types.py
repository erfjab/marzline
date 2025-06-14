from pydantic import BaseModel


class MarzneshinToken(BaseModel):
    access_token: str
    is_sudo: bool
    token_type: str = "bearer"


class MarzneshinAdmin(BaseModel):
    username: str
    is_sudo: bool
    enabled: bool = True

    @property
    def is_active(self) -> bool:
        return self.is_sudo and self.enabled
