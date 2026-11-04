from django.urls import path

from .views import (
    SkillListView,
    StudentSkillListCreateView,
    StudentSkillDetailView,
)


urlpatterns = [
    # Skill catalogue
    path(
        "skills/",
        SkillListView.as_view(),
        name="skill-list",
    ),

    # Student skills
    path(
        "students/me/skills/",
        StudentSkillListCreateView.as_view(),
        name="student-skill-list",
    ),

    path(
        "students/me/skills/<int:pk>/",
        StudentSkillDetailView.as_view(),
        name="student-skill-detail",
    ),
]