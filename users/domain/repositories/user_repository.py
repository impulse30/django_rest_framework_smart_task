from abc import ABC, abstractmethod


class UserRepository(ABC):
    """
    Interface abstraite pour le dépôt d'utilisateurs.
    Cette couche ne dépend d'aucune technologie (ORM, base de données, etc.)
    """

    @abstractmethod
    def create_user(self, email: str, password: str, full_name: str):
        """Crée un nouvel utilisateur"""
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Vérifie si un utilisateur existe avec cet email"""
        pass
