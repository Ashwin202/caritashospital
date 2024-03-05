from caritasapp.models import HomeCare
from caritasapp.lib.sendMail import sendMail
from datetime import datetime


def process_home_care_form():
    to_email = "ericjohn26296@gmail.com"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        homecare_to_process = HomeCare.objects.filter(send_status=False)
        for homecare in homecare_to_process:
            first_name = homecare.first_name
            last_name = homecare.last_name
            email = homecare.email
            phone_number = homecare.phone_number
            package = homecare.package

            body = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone Number: {phone_number}\nHealth Care Package: {package}"

            print(f"[{timestamp} | process_home_care_form] | Email body: {body}")
            sendMail(
                email,
                to_email,
                body,
                "Caritas - Response from Home Care Form",
            )
            homecare.send_status = True  # Update status to 1
            homecare.save()

    except Exception as e:
        print(
            f"[{timestamp} | process_home_care_form] | Error processing homecare packages: {e}"
        )


if __name__ == "__main__":
    process_home_care_form()
