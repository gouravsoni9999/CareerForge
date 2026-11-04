from django.urls import path
from .views import (
    StudentProfileView,
    RecruiterProfileView,
    StudentResumeDetailView,
    StudentResumeListCreateView,
)

urlpatterns = [
    path(
        "students/me/",
        StudentProfileView.as_view(),
        name="student-profile",
    ),
    path(
        "recruiters/me/",
        RecruiterProfileView.as_view(),
        name="recruiter-profile",
    ),
    path(
        "students/me/resumes/",
        StudentResumeListCreateView.as_view(),
        name="student-resume-list",
    ),
    path(
        "students/me/resumes/<int:pk>/",
        StudentResumeDetailView.as_view(),
        name="student-resume-detail",
    ),
]
