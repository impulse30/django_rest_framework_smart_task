import abc
from users.domain.entities.user import User

class ITokenService(abc.ABC):
    """
    Interface abstraite pour le service de génération de tokens.
    """

    @abc.abstractmethod
    def generate_tokens(self, user: User) -> dict:
        ...
