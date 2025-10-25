from django.urls import path
from .views.project_views import ProjectCreateView

urlpatterns = [
    path("", ProjectCreateView.as_view(), name="project-create"),
]
