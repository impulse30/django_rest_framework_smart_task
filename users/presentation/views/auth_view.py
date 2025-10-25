from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from users.presentation.serializers.auth_serializers import RegisterSerializer, LoginSerializer
from users.application.services.auth_service import AuthService


# Instance du service d'authentification
auth_service = AuthService()


@api_view(["POST"])
def register(request):
    """
    Endpoint d'inscription utilisateur.
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        # On crée l'utilisateur à partir des données validées
        user = auth_service.register_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            full_name=serializer.validated_data["full_name"]
        )

        # Réponse cohérente et claire
        return Response({
            "message": "Utilisateur créé avec succès.",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
            }
        }, status=status.HTTP_201_CREATED)

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def login(request):
    """
    Endpoint de connexion utilisateur.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        data = auth_service.login_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )

        # Renvoie les tokens JWT + info utilisateur
        return Response(data, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_401_UNAUTHORIZED
        )
