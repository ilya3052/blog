from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        if self.get_header(request) is None:
            raw = request.COOKIES.get("access_token")
            if raw:
                return self.get_user(self.get_validated_token(raw)), None
        return super().authenticate(request)