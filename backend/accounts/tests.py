
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from profiles.models import StudentProfile, RecruiterProfile


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.me_url = "/api/auth/me/"

        self.student_data = {
            "email": "student@example.com",
            "first_name": "Test",
            "last_name": "Student",
            "role": "STUDENT",
            "password": "TestPass!9876",
            "password2": "TestPass!9876",
        }

    def test_student_registration_creates_profile(self):
        response = self.client.post(
            self.register_url,
            self.student_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(email="student@example.com").exists()
        )
        self.assertTrue(
            StudentProfile.objects.filter(
                user__email="student@example.com"
            ).exists()
        )

    def test_recruiter_registration_creates_profile(self):
        data = {
            **self.student_data,
            "email": "recruiter@example.com",
            "role": "RECRUITER",
        }

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            RecruiterProfile.objects.filter(
                user__email="recruiter@example.com"
            ).exists()
        )

    def test_registration_rejects_mismatched_passwords(self):
        data = {
            **self.student_data,
            "password2": "DifferentPass!9876",
        }

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            User.objects.filter(email="student@example.com").exists()
        )

    def test_registration_rejects_admin_role(self):
        data = {
            **self.student_data,
            "role": "ADMIN",
        }

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_tokens_and_user_details(self):
        User.objects.create_user(
            email="student@example.com",
            password="TestPass!9876",
            role=User.Role.STUDENT,
        )

        response = self.client.post(
            self.login_url,
            {
                "email": "student@example.com",
                "password": "TestPass!9876",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["role"], "STUDENT")

    def test_current_user_requires_authentication(self):
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_current_user_returns_authenticated_user(self):
        user = User.objects.create_user(
            email="student@example.com",
            password="TestPass!9876",
            role=User.Role.STUDENT,
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "student@example.com")
        self.assertEqual(response.data["role"], "STUDENT")