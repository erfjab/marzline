from abc import ABC, abstractmethod


class ClientBase(ABC):
    """Base class to enforce implementation of all required methods."""

    @abstractmethod
    def generate_access_token(self):
        pass

    @abstractmethod
    def get_admin(self):
        pass

    @abstractmethod
    def get_configs(self):
        pass

    @abstractmethod
    def get_user(self):
        pass

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def create_user(self):
        pass

    @abstractmethod
    def update_user(self):
        pass

    @abstractmethod
    def remove_user(self):
        pass
