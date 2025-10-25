import uuid
from datetime import datetime

class Project:
    """
    Entité représentant un projet dans le domaine.
    """
    def __init__(
        self,
        id,
        name,
        description,
        owner_id,
        created_at=None,
        updated_at=None,
    ):
        self.id = id or uuid.uuid4()
        self.name = self._validate_name(name)
        self.description = description
        self.owner_id = owner_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def _validate_name(self, name):
        if not name or len(name.strip()) < 3:
            raise ValueError("Le nom du projet doit contenir au moins 3 caractères.")
        return name.strip()

    def __eq__(self, other):
        return isinstance(other, Project) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
