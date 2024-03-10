from caritasapp.models import Application, Career
from caritasapp.lib.send_doc_email import sendMail
from datetime import datetime

def process_application():
    to_email = 'career@caritashospital.org'
    # to_email = 'ericjohn26296@gmail.com'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        application_to_process = Application.objects.filter(send_status=False)
        for application in application_to_process:
            first_name = application.first_name
            last_name = application.last_name
            email = application.email
            phone_number = application.phone_number
            job_title_id = application.job_title
            resume = application.resume
            
            try:
                job_title_obj = Career.objects.get(id=job_title_id)
                job_title = job_title_obj.job_title
            except Career.DoesNotExist:
                job_title = 'Unknown Job Title'
            
            body = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone Number: {phone_number}\nJob Title: {job_title}"
            
            print(f"[{timestamp} | process_application] | Sending Email from {email}")
            
            sendMail(email, to_email, body, f"Caritas - Response from Application Form for {job_title}", resume)            
            application.send_status = True # Update status to 1
            application.save()

    except Exception as e:
        print(f"[{timestamp} | process_application] | Error processing application: {e}")

if __name__ == "__main__":
    process_application()