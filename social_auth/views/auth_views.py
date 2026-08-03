from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

from social_auth.serializers.auth_serializers import UserRegisterSerializer


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = RefreshToken.for_user(user)
            response = Response({"id": user.pk}, status=status.HTTP_201_CREATED)
            response.set_cookie("access_token", str(tokens.access_token))
            response.set_cookie("refresh_token", str(tokens))
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        access_token = response.data["access"]
        refresh_token = response.data["refresh"]

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=5 * 60,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=24 * 60 * 60,
        )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        if 'refresh_token' in request.COOKIES:
            request.data['refresh'] = request.COOKIES['refresh_token']
        elif 'access_token' in request.COOKIES:
            request.data['access'] = request.COOKIES['access_token']

        response = super().post(request, *args, **kwargs)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=24 * 60 * 60,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=24 * 60 * 60,
        )

        return response


class CookieTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        if 'refresh_token' in request.COOKIES:
            request.data['token'] = request.COOKIES['refresh_token']
        elif 'access_token' in request.COOKIES:
            request.data['token'] = request.COOKIES['access_token']
        return super().post(request, *args, **kwargs)


class CookieTokenBlacklist(TokenBlacklistView):
    def post(self, request: Request, *args, **kwargs):
        request.data["refresh"] = request.COOKIES["refresh_token"]
        response = super().post(request, *args, **kwargs)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


cookie_token_obtain_pair = CookieTokenObtainPairView.as_view()
cookie_token_refresh = CookieTokenRefreshView.as_view()
cookie_token_verify = CookieTokenVerifyView.as_view()
cookie_token_blacklist = CookieTokenBlacklist.as_view()
