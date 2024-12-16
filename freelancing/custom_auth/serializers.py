from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from freelancing.custom_auth.models import ApplicationUser, CustomPermission
from freelancing.utils.validation import UniqueNameMixin

from freelancing.utils.email_send import Util

from django.template.loader import render_to_string
# reset password useing email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError

User = get_user_model()


class UserAuthSerializer(serializers.Serializer):
    LOGIN_TYPE = (
        ("S", _("Simple")),
        ("A", _("Apple")),
        ("F", _("Facebook")),
        ("G", _("Google")),
    )

    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    firebase_uid = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    login_type = serializers.ChoiceField(required=True, choices=LOGIN_TYPE)

    LOGIN_TYPE_DICT = dict(LOGIN_TYPE)

    def validate(self, attrs):
        login_type = attrs.get('login_type')
        email = attrs.get('email')
        phone = attrs.get('phone')
        password = attrs.get('password')
        firebase_uid = attrs.get('firebase_uid')

        if login_type in ['G', 'A', 'F'] and not firebase_uid:
            readable_login_type = self.LOGIN_TYPE_DICT[login_type]
            raise ValidationError(_("Enter firebase_uid for {} login").format(readable_login_type))

        elif not (email or phone or firebase_uid):
            raise ValidationError(_("Either email or phone should be provided"))

        elif email and not password:
            raise ValidationError(_("Enter password for email login"))

        elif password and not email:
            raise ValidationError(_("Enter email for password login"))

        elif phone:
            if not ApplicationUser.objects.filter(phone=phone).exists():
                raise ValidationError(_("Phone number doesn't exist"))

            elif not ApplicationUser.objects.filter(phone=phone, login_type=login_type).exists():
                raise ValidationError(_("Phone number doesn't exist with this login type"))

        return attrs
class BaseUserSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    # user_permission = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "uuid", "fullname", "email", "phone", "photo", "gender",
                    "password", "is_active")
        read_only_fields = ("uuid",)
        ref_name = "BaseUserSerializer_ref"
        
    def get_photo(self, obj):
        photo = obj.photo
        if not photo:
            return
        return UserPhotoSerializer(obj).data




    def save(self, **kwargs):
        password = self.validated_data.pop("password", None)
        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=["password"])

        return user

class UserPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(source="photo", allow_null=True)
    width = serializers.ReadOnlyField(source="width_photo", allow_null=True)
    height = serializers.ReadOnlyField(source="height_photo", allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "image", "width", "height")
        ref_name = 'UserPhotoSerializer_ref'


class PasswordValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField()

    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as ex:
            raise ValidationError(ex.messages)
        return password


# class BaseUserSerializer(serializers.ModelSerializer):
#     photo = serializers.SerializerMethodField()
#     password = serializers.CharField(write_only=True)
#     kitchen = serializers.SerializerMethodField()
#     outlet = serializers.SerializerMethodField()
#     user_permission = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ("id", "uuid", "fullname", "email", "phone", "photo", "address", "gender",
#                   "password", "kitchen", "outlet", "is_active", "user_type_name", "user_permission")
#         read_only_fields = ("uuid",)
#         ref_name = "BaseUserSerializer_ref"
        
#     def get_photo(self, obj):
#         photo = obj.photo
#         if not photo:
#             return
#         return UserPhotoSerializer(obj).data

#     def get_user_permission(self, obj):
#         from foodasso.user_management.serializers import AdminUserAccessPermissionSerializer
#         user_permissions = AdminUserAccessPermission.objects.filter(user=obj)
#         return AdminUserAccessPermissionSerializer(user_permissions, many=True).data

#     def get_kitchen(self, obj):
#         try:
#             return Kitchen.objects.filter(outlet__user=obj, kitchen_type='central').first().id
#         except:
#             return None

#     def get_user_type_name(self, obj):
#         return obj.user_type.type if obj.user_type else ''

#     def get_outlet(self, obj):
#         try:
#             return Outlet.objects.filter(user=obj).first().id
#         except:
#             return None

#     def save(self, **kwargs):
#         password = self.validated_data.pop("password", None)
#         user = super().save(**kwargs)

#         if password:
#             user.set_password(password)
#             user.save(update_fields=["password"])

#         return user


class UserStatisticSerializerMixin:
    filters_amount = serializers.ReadOnlyField()

    class Meta:
        fields = ("filters_amount",)
        ref_name = "UserStatisticSerializerMixin_ref"


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data["old_password"] == validated_data["new_password"]:
            raise ValidationError(
                _(
                    "Aww don't use the same password! For security reasons, please use a different "
                    "password to your old one"
                )
            )
        elif not self.context["request"].user.check_password(
            validated_data["old_password"]
        ):
            raise ValidationError(
                _("You've entered an incorrect old password, please try again.")
            )

        return validated_data


class CustomPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = ['id', 'name', 'is_read_access', 'is_create_access', 'is_update_access',
                  'is_delete_access', 'is_printed_access']


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    # def validate(self, attrs):
    #     email = attrs.get("email")
    #     if User.objects.filter(email=email).exists():
    #         user = User.objects.get(email=email)
    #         uid = urlsafe_base64_encode(force_bytes(user.id))
    #         print("Encoded uid: ", uid)
    #         token = PasswordResetTokenGenerator().make_token(user)
    #         print("Password reset token:", token)
    #         link = "http://127.0.0.1:8000/api/custom_auth/v1/user/reset/" + uid + "/" + token
    #         print("Password Reset Link", link)
    #         # Sent Email
    #         body = "Click Following Link to reset Passsword " + link
    #         data = {
    #             "subject": "Reset Your Password",
    #             "body": body,
    #             "to_email": user.email,
    #         }
    #         Util.send_mail(data)

    #         return attrs
    #     else:
    #         raise serializers.ValidationError("You are not a Register User!!")
    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"

            # Prepare context for the email template
            context = {
                "user": user,
                "reset_link": reset_link,
                "company_name": "Logo Inc",
                "support_email": "support@example.com",
            }

            # Render the email content
            html_content = render_to_string("../templates/password_reset_email.html", context)
            plain_text_content = f"Hi {user.username},\n\nClick the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email."

            data = {
                "subject": "Reset Your Password",
                "body_text": plain_text_content,  # Plain text body
                "body_html": html_content,  # HTML body
                "to_email": user.email,
            }
            Util.send_mail(data)
            return attrs
        else:
            raise serializers.ValidationError("You are not a registered user!")


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = attrs.get("password2")
            uid = self.context.get("uid")
            token = self.context.get("token")

            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match!!"
                )
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not Valide or Expier")

            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not Valide or Expier")

