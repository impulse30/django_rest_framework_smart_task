from rest_framework_simplejwt.tokens import RefreshToken
from users.domain.entities.user import User
from users.infrastructure.models.user_model import UserModel

class JWTTokenGenerator:
    def generate_tokens(self, user: User) -> dict:
        try:
            user_model = UserModel.objects.get(id=user.id)
            refresh = RefreshToken.for_user(user_model)
            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        except UserModel.DoesNotExist:
            raise ValueError(f"No UserModel found for user with ID {user.id}")
