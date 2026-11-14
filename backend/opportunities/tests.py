
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from profiles.models import RecruiterProfile
from companies.models import Company
from opportunities.models import Opportunity


class OpportunityWorkflowTests(APITestCase):
    def setUp(self):
        self.recruiter_user = User.objects.create_user(
            email="recruiter@test.com",
            password="TestPass!9876",
            role=User.Role.RECRUITER,
        )
        self.company = Company.objects.create(
            name="Verified Test Company",
            verification_status=Company.VerificationStatus.VERIFIED,
            location="Bhopal",
        )
        self.recruiter = RecruiterProfile.objects.create(
            user=self.recruiter_user,
            company=self.company,
        )

        self.student_user = User.objects.create_user(
            email="student@test.com",
            password="TestPass!9876",
            role=User.Role.STUDENT,
        )

        self.manage_url = "/api/opportunities/manage/"

        self.opportunity_data = {
            "title": "Python Developer Intern",
            "opportunity_type": "INTERNSHIP",
            "description": "Work on backend APIs using Python.",
            "responsibilities": "Develop and test APIs.",
            "requirements": "Python and Django basics.",
            "location": "Remote",
            "work_mode": "REMOTE",
            "openings": 2,
            "application_deadline": (
                timezone.localdate() + timedelta(days=10)
            ).isoformat(),
        }

    def test_recruiter_can_create_opportunity(self):
        self.client.force_authenticate(user=self.recruiter_user)

        response = self.client.post(
            self.manage_url,
            self.opportunity_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Opportunity.objects.count(), 1)

        opportunity = Opportunity.objects.first()
        self.assertEqual(opportunity.posted_by, self.recruiter)
        self.assertEqual(opportunity.company, self.company)
        self.assertEqual(
            opportunity.status,
            Opportunity.OpportunityStatus.DRAFT,
        )

    def test_unverified_company_cannot_create_opportunity(self):
        self.company.verification_status = (
            Company.VerificationStatus.PENDING
        )
        self.company.save()

        self.client.force_authenticate(user=self.recruiter_user)

        response = self.client.post(
            self.manage_url,
            self.opportunity_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Opportunity.objects.count(), 0)

    def test_recruiter_can_publish_draft_opportunity(self):
        opportunity = Opportunity.objects.create(
            title="Backend Intern",
            opportunity_type=Opportunity.OpportunityType.INTERNSHIP,
            description="Build backend services.",
            company=self.company,
            posted_by=self.recruiter,
            location="Remote",
            work_mode=Opportunity.WorkMode.REMOTE,
            openings=1,
            application_deadline=timezone.localdate() + timedelta(days=10),
        )

        self.client.force_authenticate(user=self.recruiter_user)

        response = self.client.post(
            f"{self.manage_url}{opportunity.id}/publish/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        opportunity.refresh_from_db()
        self.assertEqual(
            opportunity.status,
            Opportunity.OpportunityStatus.PUBLISHED,
        )
        self.assertIsNotNone(opportunity.published_at)

    def test_student_cannot_access_recruiter_opportunity_management(self):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.post(
            self.manage_url,
            self.opportunity_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_see_published_verified_opportunities(self):
        Opportunity.objects.create(
            title="Visible Internship",
            opportunity_type=Opportunity.OpportunityType.INTERNSHIP,
            description="A published opportunity.",
            company=self.company,
            posted_by=self.recruiter,
            location="Remote",
            work_mode=Opportunity.WorkMode.REMOTE,
            openings=1,
            application_deadline=timezone.localdate() + timedelta(days=10),
            status=Opportunity.OpportunityStatus.PUBLISHED,
        )

        self.client.force_authenticate(user=self.student_user)

        response = self.client.get("/api/opportunities/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Visible Internship")
