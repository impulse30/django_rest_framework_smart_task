from rest_framework_simplejwt.tokens import RefreshToken
from users.domain.entities.user import User
from data.models import User as UserModel
from users.application.services.token_service import ITokenService

class JWTTokenService(ITokenService):
    """
    Implémentation concrète du service de tokenisation avec JWT.
    """
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
