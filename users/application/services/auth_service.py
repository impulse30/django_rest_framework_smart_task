from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from users.domain.entities.user import User
from data.models import User as UserModel
from users.infrastructure.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, email, password, full_name):
        if self.user_repository.exists_by_email(email):
            raise ValueError("Un utilisateur avec cet email existe déjà.")

        password_hash = make_password(password)
        user = User(
            id=None,
            email=email,
            full_name=full_name,
            password_hash=password_hash
        )
        return self.user_repository.create_user(user)

    def login_user(self, email, password):
        user = self.user_repository.get_by_email(email)
        if not user or not check_password(password, user.password_hash):
            raise ValueError("Identifiants invalides.")

        try:
            user_model = UserModel.objects.get(id=user.id)
            refresh = RefreshToken.for_user(user_model)
            tokens = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        except UserModel.DoesNotExist:
            raise ValueError(f"No UserModel found for user with ID {user.id}")

        return {
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
            },
        }
