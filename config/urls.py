from rest_framework import permissions
from rest_framework.permissions import AllowAny
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from drf_yasg import openapi  # type: ignore
from drf_yasg.views import get_schema_view  # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication  # type: ignore

# For swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Trade Time Accounting",
        default_version='v1',
        description="API documentation for Trade Time Accounting",
        terms_of_service="https://www.yourwebsite.com/terms/",
        contact=openapi.Contact(email="contact@yourwebsite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('accounts/login/', lambda request: redirect(f'/admin/login/?next=/swagger/')),  # Redirect to admin login with next parameter
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include([
        path('registration/', include('freelancing.registrations.api_urls')),
        path('custom_auth/', include('freelancing.custom_auth.api_urls')),
        path('projects/', include('freelancing.projects.api_urls')),
    ])),
    path('i18n/', include('django.conf.urls.i18n')),  # Enable language switching
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
