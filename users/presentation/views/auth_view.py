from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.presentation.serializers.auth_serializers import RegisterSerializer, LoginSerializer
from users.application.services.auth_service import AuthService
from users.infrastructure.repositories.user_repository import UserRepository

# Injection de dépendances simplifiée
def get_auth_service():
    user_repository = UserRepository()
    return AuthService(user_repository)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            auth_service = get_auth_service()
            user = auth_service.register_user(**serializer.validated_data)
            return Response({
                "message": "Utilisateur créé avec succès.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                }
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            auth_service = get_auth_service()
            data = auth_service.login_user(**serializer.validated_data)
            return Response(data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
