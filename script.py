import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
 
from caritasapp.lib.process_contact_us_form import process_contact_us 
from caritasapp.lib.process_enquire_form import process_enquire_form 
from caritasapp.lib.process_home_care import process_home_care_form 
from caritasapp.lib.process_video_consultation_form import process_video_consultation 
from caritasapp.lib.process_application_form import process_application 
from caritasapp.lib.process_international_patient_form import process_international_patient
from caritasapp.lib.process_job_application_form import process_job_application
 
process_contact_us() # send email using contact us form data 
process_enquire_form() # send email using enquiry form data 
process_home_care_form() # send email using home care form data 
process_video_consultation() # send email using video consultation form data 
process_application() # send email using application form data
process_international_patient() # send email using international patient form data
process_job_application() # send email using job application form data
