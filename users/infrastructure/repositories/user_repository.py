from users.domain.entities.user import User
from users.infrastructure.models.user_model import UserModel
from users.infrastructure.mappers.user_mapper import UserMapper

class UserRepository:
    """
    Repository pour interagir avec les données des utilisateurs,
    en utilisant l'ORM Django (UserModel) et en retournant des entités User.
    """

    def create_user(self, user_entity: User) -> User:
        """
        Crée un nouvel utilisateur dans la base de données.
        """
        user_model = UserMapper.to_model(user_entity)
        # Le mot de passe doit être hashé avant d'être sauvegardé
        user_model.set_password(user_entity.password_hash)
        user_model.save()
        return UserMapper.to_entity(user_model)

    def get_by_email(self, email: str) -> User | None:
        """
        Récupère un utilisateur par son email.
        """
        try:
            user_model = UserModel.objects.get(email=email)
            return UserMapper.to_entity(user_model)
        except UserModel.DoesNotExist:
            return None

    def exists_by_email(self, email: str) -> bool:
        """
        Vérifie si un utilisateur existe avec l'email donné.
        """
        return UserModel.objects.filter(email=email).exists()

    def get_by_id(self, user_id) -> User | None:
        """
        Récupère un utilisateur par son ID.
        """
        try:
            user_model = UserModel.objects.get(id=user_id)
            return UserMapper.to_entity(user_model)
        except UserModel.DoesNotExist:
            return None
