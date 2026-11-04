from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsStudent, IsRecruiter
from .models import StudentProfile, RecruiterProfile
from .serializers import StudentProfileSerializer, RecruiterProfileSerializer
from .models import Resume
from .serializers_resume import ResumeSerializer


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


class StudentResumeListCreateView(generics.ListCreateAPIView):

    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Resume.objects.filter(student__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class StudentResumeDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return Resume.objects.filter(student__user=self.request.user)

    def perform_destroy(self, instance):
        # Remove the stored file as well as the database record.
        instance.file.delete(save=False)
        instance.delete()