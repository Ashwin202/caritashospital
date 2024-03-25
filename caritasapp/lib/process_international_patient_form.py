from caritasapp.models import InternationalForm
from caritasapp.lib.send_mail import sendMail
from datetime import datetime

def process_international_patient():
    to_email = 'marketing@caritashospital.org'
    # to_email = 'ericjohn26296@gmail.com'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        contacts_to_process = InternationalForm.objects.filter(send_status=False)
        for contact in contacts_to_process:
            first_name = contact.first_name
            last_name = contact.last_name
            email = contact.email
            phone_number = contact.phone_number
            country = contact.country
            

            body = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone Number: {phone_number}\nCountry: {country}"
            
            print(f"[{timestamp} | process_international_patient] | Sending Email from {email}")  
            sendMail(from_email='ericjohn26296@gmail.com', to_email=[to_email], message=body, subject='Caritas - Response from International Patient Form', cc_email=['akshaya.unnikrishnan@caritashospital.org', 'managerbandc@caritashospital.org'])        
            contact.send_status = True # Update status to 1
            contact.save()

    except Exception as e:
        print(f"[{timestamp} | process_international_patient] | Error processing contacts: {e}")

if __name__ == "__main__":
    process_international_patient()
