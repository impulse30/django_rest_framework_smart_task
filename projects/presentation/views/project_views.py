from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from projects.presentation.serializers.project_serializers import ProjectCreateSerializer
from projects.application.services.project_service import ProjectService
from projects.infrastructure.repositories.project_repository import ProjectRepository
from users.infrastructure.repositories.user_repository import UserRepository

# Injection de dépendances
def get_project_service():
    project_repository = ProjectRepository()
    user_repository = UserRepository()
    return ProjectService(project_repository, user_repository)

class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            project_service = get_project_service()
            project = project_service.create_project(
                name=serializer.validated_data["name"],
                description=serializer.validated_data.get("description", ""),
                owner_id=request.user.id
            )
            # Pour la réponse, nous allons retourner un dictionnaire simple
            # Un serializer de sortie serait idéal pour un cas plus complexe
            response_data = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "owner_id": project.owner_id,
                "created_at": project.created_at,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
