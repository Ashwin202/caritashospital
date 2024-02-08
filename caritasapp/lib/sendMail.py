
from django.core.mail import send_mail


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmail(subject, body, from_email, to_email):
    sender_email = "ashwinm.045@gmail.com"
    sender_password = "wyln hmwr yncn vece"

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    
    # Attach the body of the email
    message.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to the SMTP server (in this case, Gmail's SMTP server)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            # Start TLS for security
            server.starttls()
        
            # Login to your Gmail account
            server.login(sender_email, sender_password)
        
            # Send the email
            server.sendmail(sender_email, to_email, message.as_string())
        
        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
# def sendEmail(subject,message,from_email,to_email):
#     try:
#         send_mail(subject, message, from_email, [to_email])
#         print("Email sent successfully!")

#     except Exception as e:
#         print(f"Error sending email: {e}")

sendEmail("Test subject", "Test body", "ashes192000@gmail.com", "ashwinm.045@gmail.com")