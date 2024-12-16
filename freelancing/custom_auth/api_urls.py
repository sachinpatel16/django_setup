from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore

from freelancing.custom_auth import api
# from trade_time_accounting.custom_auth.api import UserAccessPermissionAPIView

router = routers.SimpleRouter()
router.register("v1/auth", api.UserAuthViewSet, basename="auth")
router.register("v1/users", api.UserViewSet, basename="users")
router.register("v1/custom_permission", api.CustomPermissionViewSet, basename="custom_permission")

app_name = "custom-auth"

urlpatterns = [
    # JWT Token Endpoints
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('v1/user_access_permissions/', UserAccessPermissionAPIView.as_view(), name='user-access-permissions'),
    path("v1/user/reset/", api.SendPasswordResetEmailView.as_view(), name="user_reset"),
    path(
        "v1/user/reset/<uid>/<token>/",
        api.UserPasswordResetView.as_view(),
        name="user_reset_view",
    ),
    path("", include(router.urls))
]
