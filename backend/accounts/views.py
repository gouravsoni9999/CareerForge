from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    LogoutSerializer,
)

# Create your views here.
class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class LoginView(TokenObtainPairView):
    seriarlizer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    authentication_classes = []

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message":"Successfully logged out."},
            status = status.HTTP_200_OK,
        )

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id" : user.id,
            "email" : user.email,
            "first_name" : user.first_name,
            "last_name" : user.last_name,
            "role" : user.role,
        })