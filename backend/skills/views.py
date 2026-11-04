from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsStudent

from .models import Skill, StudentSkill
from .serializers import (
    SkillSerializer,
    StudentSkillSerializer,
)


class SkillListView(generics.ListAPIView):

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


class StudentSkillListCreateView(generics.ListCreateAPIView):

    serializer_class = StudentSkillSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return StudentSkill.objects.filter(
            student__user=self.request.user
        ).select_related("skill")

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)


class StudentSkillDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = StudentSkillSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return StudentSkill.objects.filter(
            student__user=self.request.user
        ).select_related("skill")