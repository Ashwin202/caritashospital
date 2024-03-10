from caritasapp.models import ContactUs
from caritasapp.lib.sendMail import sendMail
from datetime import datetime

def process_contact_us():
    to_email = 'marketing@caritashospital.org'
    # to_email = 'ericjohn26296@gmail.com'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        contacts_to_process = ContactUs.objects.filter(send_status=False)
        for contact in contacts_to_process:
            first_name = contact.first_name
            last_name = contact.last_name
            email = contact.email
            phone_number = contact.phone_number
            message = contact.message            

            body = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone Number: {phone_number}\nMessage: {message}"
            
            print(f"[{timestamp} | process_contact_us] | Sending Email from {email}")            
            sendMail(email, to_email, body, "Caritas - Response from Contact Us Form")            
            contact.send_status = True # Update status to 1
            contact.save()

    except Exception as e:
        print(f"[{timestamp} | process_contact_us] | Error processing contacts: {e}")

if __name__ == "__main__":
    process_contact_us()
