from rest_framework_simplejwt.tokens import RefreshToken
from users.application.services.token_generator import TokenGenerator
from users.domain.entities.user import User
from users.infrastructure.models.user_model import UserModel

class JWTTokenGenerator(TokenGenerator):
    def generate_tokens(self, user: User) -> dict:
        try:
            user_model = UserModel.objects.get(id=user.id)
            refresh = RefreshToken.for_user(user_model)
            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        except UserModel.DoesNotExist:
            # Handle the case where the user model does not exist, although this should not happen in a normal flow.
            # Depending on the desired behavior, you could log an error, raise an exception, or return an empty dict.
            # For this example, let's raise a ValueError to indicate a problem.
            raise ValueError(f"No UserModel found for user with ID {user.id}")
