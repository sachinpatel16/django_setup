from django.db.models import ProtectedError
from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from cryptography.fernet import Fernet


class DeleteMixin:
    def destroy(self, request, *args, **kwargs):
        """
            Set validation for delete object
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError as e:
            raise ValidationError(_('Unable to delete this record because it is being used in other records.'))
        except Http404 as e:
            raise ValidationError(_('No data matches the given query.'))
        except Exception as e:
            raise ValidationError(_(str(e)))





