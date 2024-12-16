from django.conf import settings
import logging
from templated_email import send_templated_mail
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError

import os


# class Util:
#     @staticmethod
#     def send_mail(data):
#         email = EmailMessage(
#             subject=data["subject"],
#             body=data["body"],
#             from_email=os.environ.get("EMAIL_FROM"),
#             to=[data["to_email"]],
#         )
#         email.send()
# Set up logging


class Util:
    @staticmethod
    def send_mail(data):
        """
        Sends an email using the provided data dictionary.
        Supports plain text and HTML email bodies.
        Handles exceptions and logs errors if email sending fails.
        """
        try:
            email = EmailMessage(
                subject=data["subject"],
                body=data.get("body_text", ""),  # Fallback to plain text body
                from_email=os.environ.get("EMAIL_FROM"),
                to=[data["to_email"]],
            )
            
            # Add HTML content if provided
            if "body_html" in data:
                email.content_subtype = "html"
                email.body = data["body_html"]

            # Send email
            email.send()

        except Exception as e:
            raise ValidationError(str(e))
        

# def sub_admin_reset_password_mail(user, reset_link):
#     send_templated_mail(
#         template_name="sub_admin_reset_password",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[
#             user.email,
#         ],
#         # cc=['poriyav7@gmail.com'],  # Add CC recipients here
#         bcc=settings.BCC_LIST,
#         context={
#             "user": user,
#             "reset_link": reset_link,
#             "protocol": "https"
#             if getattr(settings, "FRONTEND_USE_HTTPS", False)
#             else "http",
#         },
#     )
    # return user


# def send_email_download_student(email, first_name):
#     send_templated_mail(
#         template_name="download_mail",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[
#             email,
#         ],
#         bcc=settings.BCC_LIST,
#         context={
#             "email": email,
#             "first_name": first_name,
#             "base_url": settings.PROJECT_BASE_URL,
#             "protocol": "https"
#             if getattr(settings, "FRONTEND_USE_HTTPS", False)
#             else "http",
#         },
#     )


# def verify_otp_sing_up(email, otp):
#     send_templated_mail(
#         template_name="verify_otp_sing_up",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[
#             email,
#         ],
#         bcc=settings.BCC_LIST,
#         context={
#             "email": email,
#             "first_name": "Student",
#             "otp": otp,
#             "base_url": settings.PROJECT_BASE_URL,
#             "protocol": "https"
#             if getattr(settings, "FRONTEND_USE_HTTPS", False)
#             else "http",
#         },
#     )


# def sing_up_successful(user, password):
#     send_templated_mail(
#         template_name="singup_successful",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[
#             user.email,
#         ],
#         bcc=settings.BCC_LIST,
#         context={
#             "user": user,
#             "first_name": user.first_name,
#             "password": password,
#             "title_subject": "Successful SIGNUP – ACTIVITY POINTS ENGG APP",
#             "base_url": settings.PROJECT_BASE_URL,
#             "protocol": "https"
#             if getattr(settings, "FRONTEND_USE_HTTPS", False)
#             else "http",
#         },
#     )


# def forget_password_otp(user, otp):
#     send_templated_mail(
#         template_name="forget_password_otp",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[
#             user.email,
#         ],
#         bcc=settings.BCC_LIST,
#         context={
#             "user": user,
#             "otp": otp,
#             "first_name": user.first_name if user.first_name else "Student",
#             "title_subject": "PASSWORD Reset OTP – ACTIVITY POINTS ENGG APP",
#             "base_url": settings.PROJECT_BASE_URL,
#             "protocol": "https"
#             if getattr(settings, "FRONTEND_USE_HTTPS", False)
#             else "http",
#         },
#     )


# def send_notification_email(user, title, message):
#     send_templated_mail(
#         template_name="notification_email",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[
#             user.email,
#         ],
#         bcc=settings.BCC_LIST,
#         context={
#             "user": user,
#             "first_name": user.first_name if user.first_name else "Student",
#             "title_subject": title,
#             "message": message,
#             "base_url": settings.PROJECT_BASE_URL,
#             "protocol": "https"
#             if getattr(settings, "FRONTEND_USE_HTTPS", False)
#             else "http",
#         },
#     )


# def send_promotional_email(user, subject, body):
#     send_templated_mail(
#         template_name="promotional_email",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[],
#         bcc=user,
#         context={
#             "user": user,
#             # 'first_name': user.first_name if user.first_name else "Student",
#             "title_subject": "Promotional Email",
#             "subject": subject,
#             "body": body,
#             "base_url": settings.PROJECT_BASE_URL,
#             "protocol": "https"
#             if getattr(settings, "FRONTEND_USE_HTTPS", False)
#             else "http",
#         },
#     )
