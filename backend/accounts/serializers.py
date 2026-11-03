from django.contrib.auth import authenticate
from django.db import transaction

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from profiles.models import StudentProfile, RecruiterProfile

from .models import User

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length = 8, style = {"input_type":"password"})
    password2 = serializers.CharField(write_only = True, min_length = 8, style = {"input_type":"password"})

    class Meta:
        model = User

        fields = (
            "id", "email", "first_name", "last_name", "role", "password", "password2",
        )

        read_only_fields = ("id", )

    def validate_email(self, value):
        return value.strip().lower()

    def validate_role(self, value):
        allowed_roles = [
            User.Role.STUDENT,
            User.Role.RECRUITER,
        ]

        if value not in allowed_roles:
            raise serializers.ValidationError("You can register only as a student or recruiter.")

        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({
                "password2": "Passwords do not match."
            })

        try:
            validate_password(attrs["password"])

        except DjangoValidationError as error:
            raise serializers.ValidationError({
                "password" : error.messages
            })

        return attrs

    @transaction.atomic
    def create(self, vaidated_data):
        self.validated_data.pop("password2")

        password = self.validated_data.pop("password")

        user = User.objects.create_user(password=password, **self.validated_data,)

        if user.role == User.Role.STUDENT:
            StudentProfile.objects.create(user = user)

        elif user.role == User.Role.RECRUITER:
            RecruiterProfile.objects.create(user = user)

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["role"] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id" : self.user.id,
            "email" : self.user.email,
            "first_name" : self.user.first_name,
            "last_name" : self.user.last_name,
            "role" : self.user.role, 
        }

        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):

        try:
            token = RefreshToken(attrs["refresh"])
            token.blacklist()

        except Exception:
            raise serializers.ValidationError({"refresh": "Invalid or expired refresh token."})

        return attrs
