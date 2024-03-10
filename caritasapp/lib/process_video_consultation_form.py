from caritasapp.models import BookConsultation
from caritasapp.lib.sendMail import sendMail
from datetime import datetime


def process_video_consultation():
    to_email = "marketing@caritashospital.org"
    # to_email = 'ericjohn26296@gmail.com'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        contacts_to_process = BookConsultation.objects.filter(send_status=False)
        for contact in contacts_to_process:
            first_name = contact.first_name
            last_name = contact.last_name
            email = contact.email
            dob = contact.dob
            country = contact.country
            op_number = contact.op_number
            department = contact.department
            doctor = contact.doctor
            message = contact.message
            phone_number = contact.phone_number

            body = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone Number: {phone_number}\nDate of Birth: {dob}\nCountry: {country}\nOP Number: {op_number}\nDepartment: {department}\nDoctor: {doctor}\nMessage: {message}"

            print(
                f"[{timestamp} | process_video_consultation] | Sending Email from {email}"
            )
            sendMail(
                email, to_email, body, "Caritas - Response from Video Consultation Form"
            )
            contact.send_status = True  # Update status to 1
            contact.save()

    except Exception as e:
        print(
            f"[{timestamp} | process_video_consultation] | Error processing contacts: {e}"
        )


if __name__ == "__main__":
    process_video_consultation()
