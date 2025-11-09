from projects.domain.entities import Project, ProjectMember
from data.models import Project as ProjectModel, ProjectMember as ProjectMemberModel
from projects.infrastructure.mappers.project_mapper import ProjectMapper
from projects.infrastructure.mappers.project_member_mapper import ProjectMemberMapper

class ProjectRepository:
    def create_project(self, project_entity: Project) -> Project:
        project_model = ProjectMapper.to_model(project_entity)
        project_model.save()
        return ProjectMapper.to_entity(project_model)

    def add_member(self, member_entity: ProjectMember) -> ProjectMember:
        member_model = ProjectMemberMapper.to_model(member_entity)
        member_model.save()
        return ProjectMemberMapper.to_entity(member_model)

    def find_by_id(self, project_id: str) -> Project | None:
        try:
            project_model = ProjectModel.objects.get(id=project_id)
            return ProjectMapper.to_entity(project_model)
        except ProjectModel.DoesNotExist:
            return None
