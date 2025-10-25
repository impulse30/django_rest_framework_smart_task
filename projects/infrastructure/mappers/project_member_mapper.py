from projects.domain.entities.project_member import ProjectMember
from projects.infrastructure.models.project_member_model import ProjectMemberModel

class ProjectMemberMapper:
    @staticmethod
    def to_entity(member_model: ProjectMemberModel) -> ProjectMember:
        return ProjectMember(
            id=member_model.id,
            project_id=member_model.project_id,
            user_id=member_model.user_id,
            role=member_model.role,
            joined_at=member_model.joined_at,
        )

    @staticmethod
    def to_model(member_entity: ProjectMember) -> ProjectMemberModel:
        return ProjectMemberModel(
            id=member_entity.id,
            project_id=member_entity.project_id,
            user_id=member_entity.user_id,
            role=member_entity.role,
        )
