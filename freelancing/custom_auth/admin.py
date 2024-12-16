from django.contrib import admin
from django.db.models import BooleanField, Case, Value, When

from freelancing.custom_auth.models import (ApplicationUser, MultiToken,
                                            UserActivity, CustomPermission)

# Register your models here.
# admin.site.register(MultiToken)
# admin.site.register()
admin.site.register(UserActivity)
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone

User = get_user_model()


@admin.register(MultiToken)
class MultiTokenAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "MultiToken",
            {
                "fields": (
                    "user",
                    "key",
                    "created",
                )
            },
        ),
    )
    list_display = ("user", "key", "created")
    readonly_fields = ("user", "key", "created")
    search_fields = ("user",)


@admin.register(User)
class UserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "uuid",
                    "username",
                    "first_name",
                    "last_name",
                    "fullname",
                    "email",
                    "phone",
                    "password",
                    "gender",
                    "user_type",
                    "login_type",
                    # "date_of_birth",
                )
            },
        ),
        (
            "Statuses",
            {
                "fields": (
                    "is_active",
                    "is_email_verified",
                )
            },
        ),
        (
            "Service",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                )
            },
        ),  # 'groups', 'user_permissions'
        (
            "Account dates",
            {
                "fields": (
                    "date_joined",
                    "last_login",
                    "last_user_activity",
                    "last_modified",
                )
            },
        ),
        ("Photo", {"fields": (("photo", "width_photo", "height_photo"),)}),
        # (
        #     "Extra",
        #     {
        #         "fields": (
        #             "about",
        #             "city",
        #         )
        #     },
        # ),
    )
    readonly_fields = (
        "uuid",
        "username",
        "first_name",
        "last_name",
        "last_modified",
    )
    list_display = (
        "username",
        "fullname",
        "email",
        "_get_password",
        "date_joined",
        "uuid",
        "last_user_activity",
        "is_online",
    )
    search_fields = ("username", "email", "uuid", "fullname", "phone")

    def _get_password(self, obj):
        return "Yes" if obj.password not in [None, ""] else "No"

    _get_password.short_description = "PASSWORD"
    _get_password.admin_order_field = "password"

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term != "":
            queryset |= self.model.objects.filter(phone=search_term)

        return queryset, use_distinct

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                is_online=Case(
                    When(
                        last_user_activity__gte=timezone.now() - timedelta(minutes=5),
                        then=Value(True),
                    ),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        )

    def is_online(self, obj):
        return obj.is_online

    is_online.boolean = True
    is_online.admin_order_field = "is_online"


admin.site.register(CustomPermission)