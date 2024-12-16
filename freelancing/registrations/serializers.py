import phonenumbers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer


from freelancing.custom_auth.models import ApplicationUser

from phonenumber_field.serializerfields import PhoneNumberField



class CheckEmailSerializer(Serializer):
    email = serializers.EmailField(required=True)


class VerificationOtpSerializer(Serializer):
    phone = PhoneNumberField(required=True)
    otp = serializers.IntegerField(required=True)


class CheckOtp(Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=4, required=True)


class CheckUserDataSerializer(ModelSerializer):
    LOGIN_TYPE = (
        ("S", _("Simple")),
        ("A", _("Apple")),
        ("F", _("Facebook")),
        ("G", _("Google")),
    )

    login_type = serializers.ChoiceField(required=True, choices=LOGIN_TYPE)

    class Meta:
        model = ApplicationUser
        fields = ("email", "phone", "login_type", "social_key")
        extra_kwargs = {
            "email": {"required": False},
            "phone": {"required": False},
            "social_key": {"required": False},
            "login_type": {"required": True},
        }

    LOGIN_TYPE_DICT = dict(LOGIN_TYPE)

    def validate(self, attrs):
        login_type = attrs.get('login_type')
        email = attrs.get('email')
        phone = attrs.get('phone')
        # social_key = attrs.get('social_key')
        firebase_uid = attrs.get('firebase_uid')

        if login_type in ['G', 'A', 'F'] and not firebase_uid:
            readable_login_type = self.LOGIN_TYPE_DICT[login_type]
            raise ValidationError(_("Enter firebase_uid for {} registration").format(readable_login_type))

        elif not email:
            raise ValidationError(_("email should be provided"))

        elif not phone:
            raise ValidationError(_("phone should be provided"))

        return super().validate(attrs)


class RegistrationSerializer(ModelSerializer):

    class Meta:
        model = ApplicationUser
        fields = ("username", "fullname", "email", "phone", "password",
                "is_active", "uuid"
                )
        extra_kwargs = {
            "password": {"write_only": True, "validators": [validate_password]},
            "email": {"required": True},
            "fullname": {"required": True},
            "phone": {"required": True},
            "assign_user_roll": {"required": True}
        }
        read_only_fields = ("uuid",)

    @transaction.atomic
    def create(self, validated_data):

        validated_data['readable_password'] = validated_data.get('password')
        password = validated_data.pop("password", None)

        # create user
        user = super().create(validated_data)

        # Create related instances using the helper method
        # password assignment
        user.set_password(password)
        user.save(update_fields=["password"])

        return user