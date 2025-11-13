from users.domain.entities.user import User
from data.models import User as UserModel
from users.infrastructure.mappers.user_mapper import UserMapper

class UserRepository:
    def create_user(self, user_entity: User) -> User:
        user_model = UserMapper.to_model(user_entity)
        # Le mot de passe est déjà haché dans le service, on le sauvegarde tel quel.
        user_model.password = user_entity.password_hash
        user_model.save()
        return UserMapper.to_entity(user_model)

    def get_by_email(self, email: str) -> User | None:
        try:
            user_model = UserModel.objects.get(email=email)
            return UserMapper.to_entity(user_model)
        except UserModel.DoesNotExist:
            return None

    def exists_by_email(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

    def get_by_id(self, user_id) -> User | None:
        try:
            user_model = UserModel.objects.get(id=user_id)
            return UserMapper.to_entity(user_model)
        except UserModel.DoesNotExist:
            return None
