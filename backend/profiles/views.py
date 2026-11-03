from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsStudent, IsRecruiter
from .models import StudentProfile, RecruiterProfile
from .serializers import StudentProfileSerializer, RecruiterProfileSerializer


# Create your views here.
class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    http_method_names = ["get", "patch", "head", "options"]

    def get_object(self):
        return StudentProfile.objects.select_related("user").get(user=self.request.user)


class RecruiterProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RecruiterProfileSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
    http_method_names = ["get", "patch", "head", "options"]

    def get_object(self):
        return RecruiterProfile.objects.select_related(
            "user",
            "company",
        ).get(user=self.request.user)
