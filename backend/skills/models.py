from django.db import models

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class StudentSkill(models.Model):

    class Proficiency(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"
        EXPERT = "EXPERT", "Expert"

    student = models.ForeignKey("profiles.StudentProfile", on_delete=models.CASCADE, related_name="student_skills",)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT, related_name="student_skills",)
    proficiency = models.CharField(max_length=20, choices=Proficiency.choices, default=Proficiency.BEGINNER)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["skill__name"]

        constraints = [
            models.UniqueConstraint(
                fields=["student", "skill"],
                name="unique_student_skill",
            ),
        ]

    def __str__(self):
        return f"{self.student.user.email} - {self.skill.name}"