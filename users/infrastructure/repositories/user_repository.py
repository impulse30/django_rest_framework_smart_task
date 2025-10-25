from users.domain.entities.user import User


class UserRepository:
    """
    Repository permettant d'interagir avec le modèle User
    sans dépendre directement de l'ORM dans la couche Application.
    """

    @staticmethod
    def create_user(**validated_data):
        return User.objects.create_user(**validated_data)

    @staticmethod
    def get_by_email(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    def exists_by_email(email):
        return User.objects.filter(email=email).exists()
