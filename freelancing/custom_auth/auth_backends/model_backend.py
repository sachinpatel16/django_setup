from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.translation import gettext as _

from rest_framework.exceptions import PermissionDenied


class CustomModelBackend(ModelBackend):
    """
    Authenticate user using email, phone or username
    """

    def authenticate(self, request, username=None, email=None, phone=None, password=None, **kwargs):
        if not username and not email and not phone:
            return None

        UserModel = get_user_model()

        username_query_dict = {'username__iexact': username}
        email_query_dict = {'email__iexact': email}
        phone_query_dict = {'phone': phone}

        try:
            query_filter = Q()
            if username:
                query_filter |= Q(**username_query_dict)
            if email:
                query_filter |= Q(**email_query_dict)
            if phone:
                query_filter |= Q(**phone_query_dict)

            user = UserModel.objects.get(query_filter)

            if not user.is_active:
                raise PermissionDenied(_("User is not active."))

        except UserModel.DoesNotExist:
            return None
        except Exception:
            return None
        else:
            if user.check_password(password):
                return user

        return None