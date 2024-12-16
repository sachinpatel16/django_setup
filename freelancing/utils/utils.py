import os
import random
import uuid
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Subquery
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, _get_queryset
from django.http import Http404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import firebase_admin
from firebase_admin import auth

def get_user_photo_random_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.USER_PHOTOS, uuid.uuid4(), extension)


def set_otp_reset_expiration_time():
    return timezone.now() + timezone.timedelta(minutes=5)

def set_otp_expiration_time():
    return timezone.now() + timezone.timedelta(minutes=5)

# class PrimaryKeyRelatedFieldMixin(serializers.Serializer):
#     def validate_related_fields(self, attrs, field_names):
#         """
#             convert and assign instance to id in a fields
#             :param attrs:
#             :param field_name:
#             :return:
#         """
#         for field_name in field_names:
#             if field_name in attrs:
#                 field = self.fields[field_name]
#                 if isinstance(field, serializers.PrimaryKeyRelatedField):
#                     attrs[field_name] = attrs[field_name].id if hasattr(attrs[field_name], 'id') else attrs[field_name]
#         return attrs

#     def create_related_instances(self, validated_data, model_class, related_field_names):
#         """
#             create instance
#             :param validated_data:
#             :param model_class:
#             :param related_field_name:
#             :return:
#         """
#         for related_field_name in related_field_names:
#             if related_field_name in validated_data:
#                 related_field = validated_data.pop(related_field_name)
#                 validated_data[f'{related_field_name}_id'] = related_field if isinstance(related_field,
#                                                                                          int) else related_field.id
#         return model_class.objects.create(**validated_data)

#     def update_related_instances(self, instance, validated_data, related_field_names):
#         """
#         Update instance with related fields
#         :param instance: The main instance to update
#         :param validated_data: The validated data dictionary
#         :param related_field_names: A list of related field names to update
#         :return: The updated instance
#         """
#         for related_field_name in related_field_names:
#             if related_field_name in validated_data:
#                 related_field = validated_data.pop(related_field_name)
#                 related_instance = getattr(instance, related_field_name, None)

#                 if isinstance(related_field, dict):
#                     if related_instance:
#                         for attr, value in related_field.items():
#                             setattr(related_instance, attr, value)
#                         related_instance.save()
#                     else:
#                         # Handle the case where related_instance is None if necessary
#                         pass
#                 elif isinstance(related_field, int):
#                     # Ensure the related field is not None before accessing its _meta.model
#                     if related_instance:
#                         related_model_class = related_instance._meta.model
#                         related_field_instance = related_model_class.objects.get(id=related_field)
#                         setattr(instance, related_field_name, related_field_instance)
#                     else:
#                         # Handle the case where related_instance is None if necessary
#                         pass
#                 else:
#                     setattr(instance, related_field_name, related_field)

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()
#         return instance


# class CreateUpdateRelatedInstancesMixin:
#     """
#         create/update instance
#     """
#     def create_related_instance(self, serializer_class, data, **kwargs):
#         try:
#             serializer = serializer_class(data=data)
#             serializer.is_valid(raise_exception=True)
#             return serializer.save(**kwargs)
#         except Exception as e:
#             raise ValidationError(_(str(e)))

#     def update_related_instance(self, instance, serializer_class, data):
#         try:
#             serializer = serializer_class(instance=instance, data=data)
#             serializer.is_valid(raise_exception=True)
#             return serializer.save()
#         except Exception as e:
#             raise ValidationError(_(str(e)))


