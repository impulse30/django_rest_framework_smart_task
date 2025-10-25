from users.domain.entities.user import User
from users.infrastructure.models.user_model import UserModel

class UserMapper:
    @staticmethod
    def to_entity(user_model: UserModel) -> User:
        """Convertit un UserModel (Django) en une entité User (domaine)."""
        return User(
            id=user_model.id,
            email=user_model.email,
            full_name=user_model.full_name,
            password_hash=user_model.password,
            avatar=user_model.avatar.url if user_model.avatar else None,
            is_active=user_model.is_active,
            is_staff=user_model.is_staff,
            date_joined=user_model.date_joined,
        )

    @staticmethod
    def to_model(user_entity: User) -> UserModel:
        """Convertit une entité User (domaine) en un UserModel (Django)."""
        return UserModel(
            id=user_entity.id,
            email=user_entity.email,
            full_name=user_entity.full_name,
            password=user_entity.password_hash,
            is_active=user_entity.is_active,
            is_staff=user_entity.is_staff,
            date_joined=user_entity.date_joined,
        )
