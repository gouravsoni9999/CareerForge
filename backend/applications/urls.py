
from django.urls import path

from .views import (
    StudentApplicationListCreateView,
    StudentApplicationDetailView,
    StudentApplicationWithdrawView,
)

urlpatterns = [
    path(
        "",
        StudentApplicationListCreateView.as_view(),
        name="student-application-list-create",
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