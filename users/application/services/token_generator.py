import abc
from users.domain.entities.user import User

class TokenGenerator(abc.ABC):
    @abc.abstractmethod
    def generate_tokens(self, user: User) -> dict:
        ...
