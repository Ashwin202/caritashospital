from caritasapp.models import CareerEnquire
from caritasapp.lib.send_mail import sendMail
from datetime import datetime


def process_career_enquire_form():
    to_email = 'career@caritashospital.org'
    # to_email = 'ericjohn26296@gmail.com'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        enquiries_to_process = CareerEnquire.objects.filter(send_status=False)
        for enquiry in enquiries_to_process:
            name = enquiry.name
            email = enquiry.email
            phone_number = enquiry.phone_number
            message = enquiry.message
            page_url = enquiry.page_url

            body = f"First Name: {name}\nEmail: {email}\nPhone Number: {phone_number}\nMessage: {message}\nPage URL: {page_url}"

            print(f"[{timestamp} | process_career_enquire_form] | Sending Email from {email}")
            sendMail(from_email='ericjohn26296@gmail.com', to_email=[to_email], message=body, subject='Caritas - Response from Career Enquiry Form')
            enquiry.send_status = True  # Update status to 1
            enquiry.save()

    except Exception as e:
        print(f"[{timestamp} | process_career_enquire_form] | Error processing enquire: {e}")


if __name__ == "__main__":
    process_career_enquire_form()
