import abc

class PasswordHasher(abc.ABC):
    @abc.abstractmethod
    def hash(self, password: str) -> str:
        ...

    @abc.abstractmethod
    def verify(self, password_hash: str, password: str) -> bool:
        ...
