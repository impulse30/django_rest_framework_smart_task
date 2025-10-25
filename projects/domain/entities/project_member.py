import uuid
from datetime import datetime

class ProjectMember:
    """
    Entité représentant un membre d'un projet dans le domaine.
    """
    class Role:
        ADMIN = "ADMIN"
        MEMBER = "MEMBER"

    def __init__(
        self,
        id,
        project_id,
        user_id,
        role,
        joined_at=None,
    ):
        self.id = id or uuid.uuid4()
        self.project_id = project_id
        self.user_id = user_id
        self.role = self._validate_role(role)
        self.joined_at = joined_at or datetime.utcnow()

    def _validate_role(self, role):
        if role not in [self.Role.ADMIN, self.Role.MEMBER]:
            raise ValueError(f"Le rôle '{role}' est invalide.")
        return role

    def __eq__(self, other):
        return isinstance(other, ProjectMember) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
