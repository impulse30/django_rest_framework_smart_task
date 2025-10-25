from projects.domain.entities import Project, ProjectMember
from projects.infrastructure.repositories.project_repository import ProjectRepository
from users.infrastructure.repositories.user_repository import UserRepository

class ProjectService:
    def __init__(self, project_repository: ProjectRepository, user_repository: UserRepository):
        self.project_repository = project_repository
        self.user_repository = user_repository

    def create_project(self, name: str, description: str, owner_id: str) -> Project:
        # Vérifier si le propriétaire existe
        owner = self.user_repository.get_by_id(owner_id)
        if not owner:
            raise ValueError("Le propriétaire du projet n'existe pas.")

        # Créer l'entité projet
        project = Project(
            id=None,
            name=name,
            description=description,
            owner_id=owner_id
        )

        # Sauvegarder le projet
        created_project = self.project_repository.create_project(project)

        # Ajouter le propriétaire comme premier membre avec le rôle d'admin
        member = ProjectMember(
            id=None,
            project_id=created_project.id,
            user_id=owner_id,
            role=ProjectMember.Role.ADMIN
        )
        self.project_repository.add_member(member)

        return created_project
