from projects.domain.entities.project import Project
from projects.infrastructure.models.project_model import ProjectModel

class ProjectMapper:
    @staticmethod
    def to_entity(project_model: ProjectModel) -> Project:
        return Project(
            id=project_model.id,
            name=project_model.name,
            description=project_model.description,
            owner_id=project_model.owner_id,
            created_at=project_model.created_at,
            updated_at=project_model.updated_at,
        )

    @staticmethod
    def to_model(project_entity: Project) -> ProjectModel:
        return ProjectModel(
            id=project_entity.id,
            name=project_entity.name,
            description=project_entity.description,
            owner_id=project_entity.owner_id,
        )
