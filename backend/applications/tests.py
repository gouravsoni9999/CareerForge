
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from profiles.models import StudentProfile, RecruiterProfile
from companies.models import Company
from opportunities.models import Opportunity
from applications.models import Application


class ApplicationWorkflowTests(APITestCase):
    def setUp(self):
        self.student_user = User.objects.create_user(
            email="student@test.com",
            password="TestPass!9876",
            role=User.Role.STUDENT,
        )
        self.student = StudentProfile.objects.create(
            user=self.student_user
        )

        self.recruiter_user = User.objects.create_user(
            email="recruiter@test.com",
            password="TestPass!9876",
            role=User.Role.RECRUITER,
        )

        self.company = Company.objects.create(
            name="CareerForge Test Company",
            verification_status=Company.VerificationStatus.VERIFIED,
        )

        self.recruiter = RecruiterProfile.objects.create(
            user=self.recruiter_user,
            company=self.company,
        )

        self.opportunity = Opportunity.objects.create(
            title="Python Developer Intern",
            opportunity_type=Opportunity.OpportunityType.INTERNSHIP,
            description="Backend development internship.",
            company=self.company,
            posted_by=self.recruiter,
            location="Remote",
            work_mode=Opportunity.WorkMode.REMOTE,
            openings=2,
            application_deadline=timezone.localdate() + timedelta(days=10),
            status=Opportunity.OpportunityStatus.PUBLISHED,
        )

        self.application_url = "/api/applications/"

    def test_student_can_apply(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.post(
            self.application_url,
            {
                "opportunity": self.opportunity.id,
                "cover_letter": "I am interested in this internship.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(
            Application.objects.first().student,
            self.student,
        )

    def test_student_cannot_apply_twice(self):
        Application.objects.create(
            student=self.student,
            opportunity=self.opportunity,
        )

        self.client.force_authenticate(user=self.student_user)

        response = self.client.post(
            self.application_url,
            {"opportunity": self.opportunity.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(), 1)

    def test_student_cannot_apply_to_expired_opportunity(self):
        self.opportunity.application_deadline = (
            timezone.localdate() - timedelta(days=1)
        )
        self.opportunity.save()

        self.client.force_authenticate(user=self.student_user)

        response = self.client.post(
            self.application_url,
            {"opportunity": self.opportunity.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(), 0)

    def test_recruiter_can_update_application_status(self):
        application = Application.objects.create(
            student=self.student,
            opportunity=self.opportunity,
        )

        self.client.force_authenticate(user=self.recruiter_user)

        response = self.client.patch(
            f"/api/applications/recruiter/{application.id}/status/",
            {
                "status": Application.ApplicationStatus.SHORTLISTED,
                "recruiter_notes": "Good technical profile.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        application.refresh_from_db()
        self.assertEqual(
            application.status,
            Application.ApplicationStatus.SHORTLISTED,
        )
        self.assertEqual(
            application.recruiter_notes,
            "Good technical profile.",
        )

    def test_student_cannot_update_recruiter_application_status(self):
        application = Application.objects.create(
            student=self.student,
            opportunity=self.opportunity,
        )

        self.client.force_authenticate(user=self.student_user)

        response = self.client.patch(
            f"/api/applications/recruiter/{application.id}/status/",
            {"status": Application.ApplicationStatus.SHORTLISTED},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_recruiter_cannot_assign_applied_status(self):
        application = Application.objects.create(
            student=self.student,
            opportunity=self.opportunity,
        )

        self.client.force_authenticate(user=self.recruiter_user)

        response = self.client.patch(
            f"/api/applications/recruiter/{application.id}/status/",
            {"status": Application.ApplicationStatus.APPLIED},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
