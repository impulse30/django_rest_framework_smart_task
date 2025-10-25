import uuid
from django.db import models
from users.infrastructure.models.user_model import UserModel
from .project_model import ProjectModel

class ProjectMemberModel(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MEMBER = "MEMBER", "Member"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Project Member"
        verbose_name_plural = "Project Members"
        unique_together = ("project", "user")
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user.email} in {self.project.name}"
