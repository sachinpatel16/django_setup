from django.urls import include, path
from rest_framework.routers import SimpleRouter
from freelancing.registrations import api

# from trade_time_accounting.registrations.api import RegistrationViewSet

router = SimpleRouter()

router.register("v1/create_user", api.RegistrationViewSet, basename="create_user")


app_name = "registration"

urlpatterns = [
    path("", include(router.urls)),
]
