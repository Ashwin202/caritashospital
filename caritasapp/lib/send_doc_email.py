import os
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime

def sendMail(from_email, to_email, message, subject, resume_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if resume_path:  # Check if resume is not None
            pdf_file_path = os.path.join(settings.MEDIA_ROOT, resume_path.name)
            try:
                with open(pdf_file_path, 'rb') as file:
                    pdf_data = file.read()
            except FileNotFoundError:
                print(f"[{timestamp} | sendMail] | PDF file not found at {pdf_file_path}.")
                return
            except Exception as e:
                print(f"[{timestamp} | sendMail] | Error reading PDF file: {e}")
                return
        else:
            print(f"[{timestamp} | sendMail] | No resume path provided.")
            return

        # Safety check
        if not settings.configured:
            configure_email_settings()

        # Send email
        try:
            email = EmailMessage(subject, message, from_email, [to_email], cc=['ashes192000@gmail.com'])
            # email = EmailMessage(subject, message, from_email, [to_email], cc=['akshaya.unnikrishnan@caritashospital.org'])
            email.attach(filename='attachment.pdf', content=pdf_data, mimetype='application/pdf')
            email.send()
            print(f"[{timestamp} | sendMail] | Email sent successfully!")
        except Exception as e:
            print(f"[{timestamp} | sendMail] | Error sending email: {e}")

    except Exception as general_e:
        print(f"[{timestamp} | sendMail] | An unexpected error occurred: {general_e}")

def configure_email_settings():
    settings.configure(
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
        EMAIL_HOST='smtp.gmail.com',
        EMAIL_PORT=587,
        EMAIL_USE_TLS=True,
        EMAIL_HOST_USER='ericjohn26296@gmail.com',
        EMAIL_HOST_PASSWORD='teyi ntre ujro rdch',
        DEFAULT_FROM_EMAIL='ashes192000@gmail.com'
    )
