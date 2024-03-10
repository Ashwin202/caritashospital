import os
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime


def sendMail(from_email, to_email, message, subject, is_enquire_form = False):
    # to_email = "ericjohn26296@gmail.com"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Manually configure Django settings
        if not settings.configured:
            settings.configure(
                EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend",
                EMAIL_HOST="smtp.gmail.com",
                EMAIL_PORT=587,
                EMAIL_USE_TLS=True,
                EMAIL_HOST_USER="ericjohn26296@gmail.com",
                EMAIL_HOST_PASSWORD="teyi ntre ujro rdch",
                DEFAULT_FROM_EMAIL="ashes192000@gmail.com",
            )
        if is_enquire_form:
            to_email_list = [to_email, "managerbandc@caritashospital.org"]
        else:
            to_email_list = [to_email]
        send_mail(subject, message, from_email, to_email_list)

        print(
            f"[{timestamp} | sendMail] | From: {from_email} | Email sent successfully!"
        )

    except Exception as e:
        print(f"[{timestamp} | sendMail] | Error sending email: {e}")
