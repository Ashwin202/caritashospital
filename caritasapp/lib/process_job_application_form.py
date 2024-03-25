from caritasapp.models import JobApply
from caritasapp.lib.send_mail import sendMail
from datetime import datetime


def process_job_application():
    to_email = "career@caritashospital.org"
    # to_email = 'ericjohn26296@gmail.com'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        job_application_to_process = JobApply.objects.filter(send_status=False)
        for application in job_application_to_process:
            first_name = application.first_name
            last_name = application.last_name
            email = application.email
            phone_number = application.phone_number
            resume = application.resume

            body = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone Number: {phone_number}"

            print(f"[{timestamp} | process_job_application] | Sending Email from {email}")
            sendMail(from_email='ericjohn26296@gmail.com', to_email=[to_email], message=body, subject="Caritas - Response from Job Application Form", resume_path=resume)

            application.send_status = True  # Update status to 1
            application.save()

    except Exception as e:
        print(
            f"[{timestamp} | process_job_application] | Error processing job application: {e}"
        )


if __name__ == "__main__":
    process_job_application()
