from users.domain.entities.user import User
from users.infrastructure.repositories.user_repository import UserRepository
from users.infrastructure.services.django_password_hasher import DjangoPasswordHasher
from users.infrastructure.services.jwt_token_generator import JWTTokenGenerator

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.password_hasher = DjangoPasswordHasher()
        self.token_generator = JWTTokenGenerator()

    def register_user(self, email, password, full_name):
        if self.user_repository.exists_by_email(email):
            raise ValueError("Un utilisateur avec cet email existe déjà.")

        password_hash = self.password_hasher.hash(password)
        user = User(
            id=None,
            email=email,
            full_name=full_name,
            password_hash=password_hash
        )
        return self.user_repository.create_user(user)

    def login_user(self, email, password):
        user = self.user_repository.get_by_email(email)
        if not user or not self.password_hasher.verify(user.password_hash, password):
            raise ValueError("Identifiants invalides.")

        tokens = self.token_generator.generate_tokens(user)
        return {
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
            },
        }
