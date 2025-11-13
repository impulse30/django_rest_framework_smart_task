from django.contrib.auth.hashers import make_password, check_password
from users.domain.entities.user import User
from users.infrastructure.repositories.user_repository import UserRepository
from users.application.services.token_service import ITokenService

class AuthService:
    def __init__(self, user_repository: UserRepository, token_service: ITokenService):
        self.user_repository = user_repository
        self.token_service = token_service

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

        tokens = self.token_service.generate_tokens(user)

        return {
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
            },
        }
