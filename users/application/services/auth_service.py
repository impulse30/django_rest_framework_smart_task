from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.infrastructure.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, email, password, full_name):
        """
        Crée un nouvel utilisateur après vérification de l'unicité de l'email.
        """
        if self.user_repository.exists_by_email(email):
            raise ValueError("Un utilisateur avec cet email existe déjà.")

        # ✅ On passe les paramètres via **kwargs pour correspondre à create_user(**validated_data)
        user = self.user_repository.create_user(
            email=email,
            password=password,
            full_name=full_name
        )
        return user

    def login_user(self, email, password):
        """
        Authentifie un utilisateur et retourne ses tokens JWT.
        """
        user = authenticate(email=email, password=password)
        if not user:
            raise ValueError("Identifiants invalides.")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
            },
        }
