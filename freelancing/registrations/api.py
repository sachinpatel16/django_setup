import random

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from templated_email import send_templated_mail
from unicef_restlib.views import MultiSerializerViewSetMixin

from freelancing.custom_auth.api import UserAuthViewSet
from freelancing.custom_auth.models import ApplicationUser, StudentOTP, MultiToken, LoginOtp
from freelancing.custom_auth.serializers import BaseUserSerializer
from freelancing.registrations.serializers import (CheckEmailSerializer,
                                                CheckUserDataSerializer,
                                                RegistrationSerializer, VerificationOtpSerializer)

from freelancing.utils.permissions import IsAPIKEYAuthenticated


class RegistrationViewSet(
    MultiSerializerViewSetMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = ApplicationUser.objects.all()
    serializer_class = RegistrationSerializer
    # renderer_classes = [MenuCategoryRenderer]
    serializer_action_classes = {
        "check_user_data": CheckUserDataSerializer,
        "send_sms": CheckEmailSerializer,
    }
    permission_classes = (AllowAny, IsAPIKEYAuthenticated,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        create token for authorization
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            user = serializer.instance

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # token, created = MultiToken.objects.get_or_create(user=user)
            data = BaseUserSerializer(instance=user).data
            # data['token'] = token.key
            data['access_token'] = access_token
            data['refresh_token'] = refresh_token
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=["post"], permission_classes=(AllowAny, IsAPIKEYAuthenticated), url_name="check",
    #         url_path="check", detail=False)
    # def check_user_data(self, *args, **kwargs):
    #     """
    #         Check email, phone and social key are already exist or not
    #     """
    #     serializer = self.get_serializer(data=self.request.data)

    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    #     return Response(serializer.data)

    # @action(methods=['post'], permission_classes=(AllowAny, IsAPIKEYAuthenticated,), url_name='check',
    #         url_path='check', detail=False)
    # def check_user_data(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=self.request.data)
    #
    #     serializer.is_valid(raise_exception=True)
    #
    #     # Send SMS code
    #     otp = random.randint(1000, 9999)
    #     email = serializer.validated_data.get("email")
    #     site = get_current_site(request)
    #
    #     # send Email
    #     send_templated_mail(
    #         template_name="reset_password",
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[email],
    #         context={
    #             'domain': site.domain,
    #             'otp': otp,
    #             # 'password_reset_id': password_reset_obj.id,
    #             'protocol': 'http',
    #             'email': email,
    #             'name': 'Registration Otp Verify',
    #         }
    #     )
    #
    #     data = serializer.data
    #     data.update({'otp': otp})
    #     return Response(data)

    # @action(permission_classes=(AllowAny, IsAPIKEYAuthenticated,), methods=["post"],
    #         url_name="send_sms_code", url_path="send-sms-code", detail=False,)
    # def send_sms(self, request, *args, **kwargs):
    #     """
    #         For manual sms code sending
    #     """
    #     serializer = self.get_serializer(data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #     email = serializer.validated_data.get("email")
    #     if ApplicationUser.objects.filter(email=email).exists():
    #         raise ValidationError(_("User already exists with this email."))
    #     # delete old otp
    #     # StudentOTP.objects.filter(email=email).delete()

    #     # creating new otp

    #     otp = random.randint(1000, 9999)
    #     # StudentOTP.objects.create(email=email, otp=otp)

    #     site = get_current_site(request)
    #     # verify_otp_sing_up(email, otp)
    #     # send Email
    #     send_templated_mail(
    #         template_name="reset_password",
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[email],
    #         context={
    #             'domain': site.domain,
    #             'otp': otp,
    #             # 'password_reset_id': password_reset_obj.id,
    #             'protocol': 'http',
    #             'email': email,
    #             'name': 'Registration Resend Otp Verify',
    #         }
    #     )

    #     data = serializer.data
    #     data.update({"otp": otp})
    #     return Response(data)

    # @action(permission_classes=(AllowAny, IsAPIKEYAuthenticated), methods=["post"],
    #         url_name="verification_otp", url_path="verification_otp", detail=False)
    # def verification_otp(self, request, *args, **kwargs):
    #     """
    #         For verify otp code sending
    #     """
    #     serializer = VerificationOtpSerializer(data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #     phone = serializer.validated_data.get("phone")
    #     otp = serializer.validated_data.get("otp")

    #     if not LoginOtp.objects.filter(user_mobile=phone).exists():
    #         raise ValidationError(_("phone number doesn't exist"))
    #     user_otp = LoginOtp.objects.filter(user_mobile=phone, otp=otp, expiration_time__gt=timezone.now()).first()

    #     if not user_otp:
    #         raise ValidationError(_("OTP not verified."))
    #     user_otp.delete()

    #     user = ApplicationUser.objects.get(phone=phone)
    #     user_details = BaseUserSerializer(instance=user, context={"request": request, "view": self}).data
    #     user_details.update(UserAuthViewSet.get_success_headers(user))

    #     return Response(data=user_details, status=status.HTTP_200_OK)
