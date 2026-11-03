from django.urls import path
from .views import StudentProfileView, RecruiterProfileView

urlpatterns = [
    path(
        "students/me/",
        StudentProfileView.as_view(),
        name = "student-profile",
    ),
    path(
        "recruiters/me/",
        RecruiterProfileView.as_view(),
        name="recruiter-profile",
    ),
]