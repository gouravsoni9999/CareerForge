from django.urls import path

from .views import (
    StudentApplicationListCreateView,
    StudentApplicationDetailView,
    StudentApplicationWithdrawView,
)

from .views_recruiter import RecruiterApplicationStatusView, RecruiterApplicationResumeView

urlpatterns = [
    path(
        "",
        StudentApplicationListCreateView.as_view(),
        name="student-application-list-create",
    ),
    path(
        "recruiter/<int:pk>/status/",
        RecruiterApplicationStatusView.as_view(),
        name="recruiter-application-status",
    ),
    path(
        "recruiter/<int:pk>/resume/",
        RecruiterApplicationResumeView.as_view(),
        name="recruiter-application-resume",
    ),
    path(
        "<int:pk>/",
        StudentApplicationDetailView.as_view(),
        name="student-application-detail",
    ),
    path(
        "<int:pk>/withdraw/",
        StudentApplicationWithdrawView.as_view(),
        name="student-application-withdraw",
    ),
]
