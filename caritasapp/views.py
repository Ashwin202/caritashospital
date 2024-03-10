from django.shortcuts import render, redirect
from .models import Post,Category,Doctor,CareerEnquire,Department,Contact,ContactUs, Career,JobType,Application,SliderImage,Videos,Album,MobileSliderImage,BioMedical, QualityControl, Studies,HomeCare,Hospital,InternationalForm,BookConsultation, CaritasHospitalDoctor,DoctorSlider
from .models import Card
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save  # Import the post_save signal
import os
from moviepy.editor import VideoFileClip 
from .models import Enquire
from .forms import EnquireForm, ContactUsForm,ApplicationForm,InternationalForm,BookConsultationForm, CareerEnquireForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import ContactForm,HomeCareForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import pycountry
from itertools import groupby 
from django.db.models import Count 
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Max
import datetime
from django.core.mail import send_mail
# from .lib.sendMail import sendEmail
from django.http import HttpResponseRedirect
from .models import JobApply
from .forms import JobApplyForm
from .models import VideoGallery

# Create your views here.
def index(request):
    posts = Post.objects.all()[:11]
    videos = Video.objects.all()
    testimonials = Videos.objects.all().order_by('-created_at')
    desktop_images = SliderImage.objects.all()
    mobile_images = MobileSliderImage.objects.all()
    doctors_images = DoctorSlider.objects.all()
    context = {
     'posts': posts,
     'videos': videos,
     'desktop_images':desktop_images ,
     'mobile_images': mobile_images,
     'testimonials':testimonials,
     'doctors_images': doctors_images,
    }
    return render(request, 'caritasapp/index.html', context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Fetch related posts based on the department of the current post
    related_posts = Post.objects.filter(department=post.department).exclude(slug=slug)[:3]
    
    context = {'post': post, 'related_posts': related_posts}
    return render(request, 'caritasapp/detail.html', context)


def display_video_list(request):
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, 'caritasapp/video_list.html', context)

# Define a signal handler to generate and save the thumbnail image when a new video is saved
@receiver(post_save, sender=Video)
def generate_video_thumbnail(sender, instance, **kwargs):
    if not instance.thumbnail:
        # Create a directory for thumbnails if it doesn't exist
        thumbnail_dir = os.path.join('media', 'video_thumbnails')
        os.makedirs(thumbnail_dir, exist_ok=True)

        # Generate a thumbnail by extracting the frame at a specified time (e.g., 5 seconds)
        video_clip = VideoFileClip(instance.file.path)
        thumbnail = video_clip.get_frame(5)  # Adjust the time as needed
        
        # Save the thumbnail image
        thumbnail_path = os.path.join(thumbnail_dir, f'{instance.title}_thumbnail.jpg')
        thumbnail.save(thumbnail_path, 'JPEG')

        # Set the thumbnail field of the Video model
        instance.thumbnail = os.path.relpath(thumbnail_path, 'media')
        instance.save()

def contact(request):
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    context = {
        'departments': departments,
        'doctors': doctors,
    }
    
    if request.method == 'POST':
        query_type = request.POST.get('query_type')
        name = request.POST.get('name')
        email = request.POST.get('email')
        department_id = request.POST.get('department') 
        doctor_id = request.POST.get('doctor')
        message = request.POST.get('message')

        # Save the form data to the database
        entry = Contact.objects.create(
            query_type=query_type,
            name=name,
            email=email,
            department_id=department_id,  # Assign department_id to the model field
            doctor_id=doctor_id,
            message=message
        )
        return render(request, 'caritasapp/success.html')
    else:
        form = ContactForm()

    return render(request, 'caritasapp/contact.html', context=context)
    
def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            entry = form.save()  # This will save the form data to the ContactUs model

            # Send email to admin
            subject = 'New Contact Us Submission'
            message = f'Name: {entry.first_name} {entry.last_name}\nEmail: {entry.email}\nPhone Number: {entry.phone_number}\nMessage: {entry.message}\nPage URL: {entry.page_url}'
            from_email = 'neeraja@onbyz.com'
            to_email = 'simy@onbyz.com'
            # send_mail(subject, message, from_email, [to_email],fail_silently=False, auth_user='ashwinm.045@gmail.com', auth_password='wyln hmwr yncn vece')
            # send_mail(subject, message, from_email, [to_email])
            # sendEmail(subject, message, from_email, to_email)
            # try:
            #     send_mail(subject, message, from_email, [to_email])
            # except Exception as e:
            #     print(f"Error sending email: {e}")

            return render(request, 'caritasapp/success.html')  # Redirect to a success page
    else:
        form = ContactUsForm()

    return render(request, 'caritasapp/contact_us.html', {'form': form})


def caritas_cancer_institute(request):
    department_name = 'Caritas Cancer Institute'
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    
    #upcoming_projects = Category.objects.get(title='Upcoming Projects')
    cancer = Category.objects.get(title='cancer')
  #  upcoming_projects_posts = Post.objects.filter(category=upcoming_projects)[:5] 
    cancer_posts = Post.objects.filter(category=cancer)[:5]
    
    context = {
       # 'upcoming_projects_posts': upcoming_projects_posts,
        'cancer_posts': cancer_posts,
        'doctors': doctors,
        'departments': departments
    }
    return render(request, 'caritasapp/caritas_cancer_institute.html', context)


def enquire_form(request):
    if request.method == 'POST':
        form = EnquireForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            page_url = request.META.get('HTTP_REFERER')  # Get the page URL

            # Save the form data to the database
            entry = Enquire.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                message=message,
                page_url=page_url,
            )

            # Redirect to a success page
            return render(request, 'caritasapp/success.html')

    else:
        form = EnquireForm()

    return render(request, 'caritasapp/caritas_cancer_institute.html', {'form': form})
    
def doctors(request):
    doctors = Doctor.objects.filter(is_visible=True).order_by('order')
    departments = Department.objects.filter(doctor__isnull=False).distinct().order_by('name')
    search_query = request.GET.get('search')
    search_results = None
    
    if search_query:
        # Perform search query based on the search query entered by the user
        search_results = Doctor.objects.filter(
            Q(name__icontains=search_query) |  # Search by doctor name
            Q(department__name__icontains=search_query) |  # Search by department name
            Q(specialization__icontains=search_query)  # Search by specialization
        )
    
    return render(request, 'doctors.html', {'doctors': doctors, 'departments': departments, 'search_query': search_query, 'search_results': search_results})

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    department = Department.objects.all()
    return render(request, 'doctor_detail.html', {'doctor': doctor, 'department': department})



def caritas_heart_institute(request):
    department_name = 'Caritas Heart Institute'
    department = Department.objects.get(name=department_name)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    cancer = Category.objects.get(title='cancer')
    posts = Post.objects.filter(department__name="Caritas Heart Institute")[:5]

    
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments
        
    }
    return render(request, 'caritasapp/caritas_heart_institute.html', context)

def caritas_neuro(request):
    department_name = 'Caritas Neuro Sciences'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Caritas Neuro Sciences")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments
    }
    return render(request, 'caritasapp/caritas_neuro.html', context)

def caritas_gastro(request):
    department_name = 'Gastro Sciences'
    department = Department.objects.get(name=department_name)
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Gastro Sciences")[:5]
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments
    }
    return render(request, 'caritasapp/caritas_gastro.html', context)

def caritas_orthopaedics(request):
    department_name = 'Orthopaedics, Joint Replacement and Arthroscopy'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Orthopaedics, Joint Replacement and Arthroscopy")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments
    }
    return render(request, 'caritasapp/caritas_orthopaedics.html', context)

def caritas_nephrology(request):
    department_name = 'Nephrology & Renal Transplant'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Nephrology & Renal Transplant")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/caritas_nephrology.html', context)

def caritas_urology(request):
    department_name = 'Urology'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Urology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/caritas_urology.html', context)

def caritas_rheumatology(request):
    department_name = 'Rheumatology'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Rheumatology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/caritas_rheumatology.html', context)

def caritas_paediatrics(request):
    department_name = 'Paediatrics & Paediatrics Surgery'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Paediatrics & Paediatrics Surgery")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/caritas_paediatrics.html', context)

def caritas_generalmedicine(request):
    department_name = 'General Medicine'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Caritas Neuro Sciences")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/caritas_generalmedicine.html', context)

def caritas_ENT(request):
    department_name = 'ENT & Audiology'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="ENT & Audiology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/caritas_ENT.html', context)

def endocrinology(request):
    department_name = 'Endocrinology'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Endocrinology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/endocrinology.html', context)

def neonatology(request):
    department_name = 'Neonatology'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Neonatology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/neonatology.html', context)

def ophthalmology(request):
    department_name = 'Ophthalmology'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Ophthalmology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/ophthalmology.html', context)
    
def emergency_medicine(request):
    department_name = 'Emergency Medicine & Trauma Care'
    department = Department.objects.get(name=department_name)
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Emergency Medicine & Trauma Care")[:5]
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/emergency_medicine.html', context)

def dental(request):
    department_name = 'Dental, Oral & Maxillo Facial Surgery'
    department = Department.objects.get(name=department_name)
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Dental, Oral & Maxillo Facial Surgery")[:5]
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/dental.html', context)

def pathology(request):
    department_name = 'Pathology, Microbiology & Laboratory Medicine'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Pathology, Microbiology & Laboratory Medicine")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/pathology.html', context)
    
def psychiatry(request):
    department_name = 'Psychiatry, Counseling and Psychotherapy Services'
    department = Department.objects.get(name=department_name)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Psychiatry, Counseling and Psychotherapy Services")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/psychiatry.html', context)
    
def plastic_microvascular(request):
    department_name = 'Plastic and Micro Vascular Surgery'
    department = Department.objects.get(name=department_name)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Plastic and Micro Vascular Surgery")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/plastic_microvascular.html', context)
    
def pulmonology(request):
    department_name = 'Pulmonology & Interventional Pulmonology'
    department = Department.objects.get(name=department_name)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Pulmonology & Interventional Pulmonology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/pulmonology.html', context)
    
  
def about_caritas(request):
    return render(request, 'caritasapp/about_caritas.html') 
    
    
def gynaecology(request):
    department_name = 'Obstetrics, Gynaecology and Fetal Medicine'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Obstetrics, Gynaecology and Fetal Medicine")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/gynaecology.html', context)
    
def dermatology(request):
    department_name = 'Dermatology & Cosmetology'
    department = Department.objects.get(name=department_name)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Pulmonology & Interventional Pulmonology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/dermatology.html', context)
    
def anaesthesiology(request):
    department_name = 'Anaesthesiology'
    department = Department.objects.get(name=department_name)
    
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Anaesthesiology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
    
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/anaesthesiology.html', context)
    
def physicalmedicine(request):
    department_name = 'Physical Medicine and Rehabilitation'
    department = Department.objects.get(name=department_name)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Pulmonology & Interventional Pulmonology")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/physicalmedicine.html', context)
    
    
def criticalcare(request):
    department_name = 'Critical Care Medicine'
    department = Department.objects.get(name=department_name)
    
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all() 
    posts = Post.objects.filter(department__name="Critical Care Medicine")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        
        
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/criticalcare.html', context)
    
def generalsurgery(request):
    department_name = 'General Surgery'
    department = Department.objects.get(name=department_name)
    
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all() 
    posts = Post.objects.filter(department__name="Caritas Neuro Sciences")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/generalsurgery.html', context)
    
def radiology(request):
    department_name = 'Interventional Radiology, Radio Diagnosis and Imaging'
    department = Department.objects.get(name=department_name)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all() 
    posts = Post.objects.filter(department__name="Caritas Neuro Sciences")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/radiology.html', context)
  
    
def blood(request):
   
    cancer = Category.objects.get(title='cancer')
    posts = Post.objects.filter(department__name="Caritas Neuro Sciences")[:5]
    context = {
        
        'posts': posts,
    }
    return render(request, 'caritasapp/blood.html', context)

def clinical(request):
    posts = Post.objects.filter(department__name="Caritas Neuro Sciences")[:5]
    context = {
        'posts': posts,
    }
    return render(request, 'caritasapp/clinical.html', context)

def physiotherapy(request):
    cancer = Category.objects.get(title='cancer')
    cancer_posts = Post.objects.filter(category=cancer)[:5]
    context = {
       
        'cancer_posts': cancer_posts,
    }
    return render(request, 'caritasapp/physiotherapy.html', context)
    
def organ(request):
   
    cancer = Category.objects.get(title='cancer')
    
    cancer_posts = Post.objects.filter(category=cancer)[:5]
    context = {
        
        'cancer_posts': cancer_posts,
    }
    return render(request, 'caritasapp/organ.html', context)
 
def insurance(request):
    cancer = Category.objects.get(title='cancer')
    cancer_posts = Post.objects.filter(category=cancer)[:5]
    context = {
        'cancer_posts': cancer_posts,
    }
    return render(request, 'caritasapp/insurance.html', context)  
    
def secondopinion(request):
    cancer = Category.objects.get(title='cancer')
     
    cancer_posts = Post.objects.filter(category=cancer)[:5]
    context = {
        'cancer_posts': cancer_posts,
    }
    return render(request, 'caritasapp/secondopinion.html', context) 

def pastoralcare(request):
    cancer = Category.objects.get(title='cancer')
    cancer_posts = Post.objects.filter(category=cancer)[:5]
    context = {
        'cancer_posts': cancer_posts,
    }
    return render(request, 'caritasapp/pastoralcare.html', context)
    
def stroke(request):
    cancer = Category.objects.get(title='cancer')
    cancer_posts = Post.objects.filter(category=cancer)[:5]
    context = {
        'cancer_posts': cancer_posts,
    }
    return render(request, 'caritasapp/stroke.html', context)
    
    
def director_message(request):
    return render(request, 'caritasapp/director-message.html') 
def governing_body(request):
     return render(request, 'caritasapp/governing_body.html')
     
def quality_control(request):
    year = request.POST.get('year')
    month = request.POST.get('month')


    if year and month:
        # Assuming month_year is a DateField or DateTimeField
        # quality = QualityControl.objects.filter(month_year__year=year, month_year__month=month)
        quality = list(QualityControl.objects.filter(month_year__year=year, month_year__month=month).values())            
        return JsonResponse({'quality': quality})       
    else:
        x = datetime.datetime.now()        
        quality = QualityControl.objects.all().order_by('-month_year')[:1].values()

    return render(request, 'caritasapp/quality_control.html', {'quality': quality})
    
    

    
def articles(request):
   
    posts = Post.objects.order_by('-created')
    departments = Department.objects.filter(post__isnull=False).distinct().order_by('name')
    videos = Video.objects.all()
    context = {
     'posts': posts,
     'videos': videos,
     'departments': departments,
    }
    return render(request, 'articles.html', context)
    
def dnb(request):
    
    cancer = Category.objects.get(title='cancer')
    
    cancer_posts = Post.objects.filter(category=cancer)[:5]
    context = {
        
        'cancer_posts': cancer_posts,
    }
    return render(request, 'caritasapp/dnb.html', context)
    
def health_package(request):
    return render(request, 'caritasapp/health_package.html') 
    
def caritasnursing(request):
    return render(request, 'caritasapp/caritasnursing.html') 
    
def pharmacy(request):
    return render(request, 'caritasapp/pharmacy.html') 

def international_patients(request):
    countries = list(pycountry.countries)
    videos = Video.objects.all()
    testimonials = Videos.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = InternationalForm(request.POST)
        if form.is_valid():
            form.save()
            # Add success logic here, like redirecting to a thank-you page
            return render(request, 'caritasapp/success.html')
    else:
        form = InternationalForm()

  
    context = {
     
     'videos': videos,
     'countries': countries,
     'testimonials': testimonials,
     'form': form,
    }
    return render(request, 'caritasapp/international_patients.html', context) 

def international_patients_arabic(request):
    countries = list(pycountry.countries)
    videos = Video.objects.all()
    testimonials = Videos.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = InternationalForm(request.POST)
        if form.is_valid():
            form.save()
            # Add success logic here, like redirecting to a thank-you page
            return render(request, 'caritasapp/success.html')
    else:
        form = InternationalForm()

  
    context = {
     
     'videos': videos,
     'countries': countries,
     'testimonials': testimonials,
     'form': form,
    }
    return render(request, 'caritasapp/international_patients_arabic.html', context) 
    
def directions(request):
    return render(request, 'caritasapp/directions.html')  
#def contact_us(request):
   # return render(request, 'caritasapp/contact_us.html')  
    
def charity(request):
    return render(request, 'caritasapp/charity.html') 
    
def career(request):
    careers = Career.objects.all()
    if request.method == 'POST':
        form = CareerEnquireForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            page_url = request.META.get('HTTP_REFERER')  # Get the page URL

            # Save the form data to the database
            entry = CareerEnquire.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                message=message,
                page_url=page_url,
            )

            # Redirect to a success page
            return render(request, 'caritasapp/success.html')

    else:
        form = CareerEnquireForm()
    return render(request, 'caritasapp/career.html', {'careers': careers})
    
def biomedical(request):
    year = request.GET.get('year')
    month = request.GET.get('month')

     # Retrieve all BioMedical objects by default
           

    if year and month:
            # Filter BioMedical objects based on the provided year and month
            data = list(BioMedical.objects.filter(month_year__year=year, month_year__month=month).values())
            return JsonResponse({'data': data})
    else:
        data = BioMedical.objects.all().order_by('-month_year')[:1].values() 
     
    
    return render(request, 'caritasapp/biomedical.html', {'data': data})
 

  
    
 
def support(request):
    return render(request,'caritasapp/support.html')

def complaints(request):
    return render(request,'caritasapp/complaints.html')
def ethics(request):
    return render(request,'caritasapp/ethics.html')   

def paramedical(request):
    return render(request,'caritasapp/paramedical.html')   
    
def family(request):
    hospital_name = 'Caritas Family Hospital'

    hospital = get_object_or_404(Hospital, name=hospital_name)
    
    doctors_in_hospital = CaritasHospitalDoctor.objects.filter(hospitals=hospital).order_by('order')

    context = {
        'doctors_in_hospital': doctors_in_hospital,
        'hospital': hospital,
    }

    return render(request, 'caritasapp/family.html', context)
    
def caritashdp(request):
    hospital_name = 'Caritas HDP Hospital'
    hospital = get_object_or_404(Hospital, name=hospital_name)
    doctors_in_hospital = CaritasHospitalDoctor.objects.filter(hospitals=hospital).order_by('order')

    context = {
        'doctors_in_hospital': doctors_in_hospital,
        'hospital': hospital,
    }

    return render(request, 'caritasapp/caritashdp.html', context)

def caritaskkm(request):
    hospital_name = 'Caritas KMM Hospital'

    hospital = get_object_or_404(Hospital, name=hospital_name)
    
    doctors_in_hospital = CaritasHospitalDoctor.objects.filter(hospitals=hospital).order_by('order')

    context = {
        'doctors_in_hospital': doctors_in_hospital,
        'hospital': hospital,
    
    }
    return render(request,'caritasapp/caritaskkm.html', context)
    
def open_positions(request):
    careers = Career.objects.all()
    job_types = JobType.objects.values_list('job_type', flat=True).distinct()
    
    if request.method == 'POST':
        form = JobApplyForm(request.POST, request.FILES)
        if form.is_valid():
            # Create an application object but don't save it yet
            application = form.save(commit=False)
            application.save()
            return render(request, 'caritasapp/success.html')  # Redirect to a success page
    else:
        form = JobApplyForm()
    context = {'careers': careers, 'form': form, 'job_types': job_types}
    return render(request,'caritasapp/open_positions.html', context)
    
def job_detail(request, career_id):
    career = get_object_or_404(Career, id=career_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create an application object but don't save it yet
            application = form.save(commit=False)
            application.job_title = career  # Assign the entire Career object to job_title
            application.save()
            return render(request, 'caritasapp/success.html')  # Redirect to a success page
    else:
        form = ApplicationForm()

    return render(request, 'caritasapp/job_details.html', {'form': form, 'career': career})
    
def senior_executive(request):
    return render(request,'caritasapp/senior_executive.html')
    

def video_consultation(request):
    doctors = Doctor.objects.all()
    departments = Department.objects.all()
    countries = list(pycountry.countries)

    if request.method == 'POST':
        form = BookConsultationForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return render(request, 'caritasapp/success.html')
        else:
            print(form.errors)
    else:
        form = BookConsultationForm()

    return render(request, 'caritasapp/video_consultation.html', {'form': form, 'doctors': doctors, 'departments': departments, 'countries': countries})

    
def homecare(request):
    if request.method == 'POST':
        form = HomeCareForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()

            # Send email notification
           # subject = 'New Home Care Inquiry'
            #message = 'A new home care inquiry has been submitted.'
            #from_email = 'your@example.com'  # Replace with your email
            #to_email = 'admin@example.com'  # Replace with admin's email
            #send_mail(subject, message, from_email, [to_email])

            # Redirect to a success page or render a success message
            return HttpResponseRedirect('/success/')  # Redirect to a success page
    else:
        form = HomeCareForm()
    return render(request, 'caritasapp/homecare.html', {'form': form})
    
def visitors_guide(request):
    return render(request, 'caritasapp/visitors_guide.html')

def milestones(request):
    return render(request, 'caritasapp/milestones.html')
    
def mortuary_services(request):
    return render(request, 'caritasapp/mortuary_services.html')
    
def privacy(request):
    return render(request, 'caritasapp/privacy.html')
    
def terms_conditions(request):
    return render(request, 'caritasapp/terms_conditions.html')
    
def achievements(request):
    return render(request, 'caritasapp/achievements.html')
    
def news_events(request):
    posts = Post.objects.all()
    
    context = {
     'posts': posts,
    }
    return render(request, 'caritasapp/news_events.html', context)
    
def search_doctors(request):
    query = request.GET.get('search', '')
    doctors = []

    if query:
        doctors = Doctor.objects.filter(name__icontains=query)

    return render(request, 'doctors.html', {'doctors': doctors, 'query': query})
    
def search_results(request):
    if request.method == 'POST':
        search = request.POST['search']
        #departments = Department.objects.filter(name__contains=search)
        departments = Department.objects.all()
        doctors = Doctor.objects.filter(
                Q(name__icontains=search) |
                Q(department__name__icontains=search)
            )


        return render(request, 'caritasapp/search_results.html', {'search': search, 'doctors':doctors,'departments':departments})
    else:
        return render(request, 'caritasapp/search_results.html', {})

def autocomplete(request):
    term = request.GET.get('term', '')
    suggestions = Doctor.objects.filter(name__icontains=term).values_list('name', flat=True)
    return JsonResponse(list(suggestions), safe=False)
    
def patients_testimonials(request):
    videos = Videos.objects.all().order_by('-created_at')
    context = {
     'videos': videos,
    }
    return render(request, 'caritasapp/patients_testimonials.html', context)
    
def search_jobs(request):
    query = request.GET.get('search')
    job_titles = []

    if query:
        job_titles = Career.objects.filter(job_title__icontains=query)

    return render(request, 'caritasapp/open_positions.html', {'job_titles': job_titles, 'query': query})
    
def gallery(request):
    albums = Album.objects.all()
    context = {'albums': albums}

    return render(request, 'caritasapp/gallery.html', context)
    
def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    context = {'album': album}
    return render(request, 'caritasapp/album_detail.html', context)

def faq(request):
    return render(request, 'caritasapp/faq.html') 
    
def testimonials(request):
    testimonials = Videos.objects.all().order_by('-created_at')
    return render(request, 'caritasapp/testimonials.html', {'testimonials': testimonials})

def community_medicine(request):
    department_name = 'Community Medicine'
    department = Department.objects.get(name=department_name)
    posts = Post.objects.filter(department__name="Community Medicine")[:5]
    cancer = Category.objects.get(title='cancer')
    doctors = Doctor.objects.all()
    departments = Department.objects.all() 
    doctors_in_department = Doctor.objects.filter(department=department)
    cancer_posts = Post.objects.filter(category=cancer)[:5]
    context = {
        
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/community_medicine.html', context)
    
    
def filter_doctors(request):
    selected_department = request.GET.get('department')

    if selected_department:
        doctors = Doctor.objects.filter(department_id=selected_department)
    else:
        doctors = Doctor.objects.all()

    return render(request, 'doctors.html', {'form': form, 'doctors': doctors})
    
def research_development(request):
    ongoing_studies = Studies.objects.filter(category="Ongoing")
    completed_studies = Studies.objects.filter(category="Completed")

    # Pagination for ongoing studies
    ongoing_paginator = Paginator(ongoing_studies, 5)
    ongoing_page_number = request.GET.get('ongoing_page')
    ongoing_page_obj = ongoing_paginator.get_page(ongoing_page_number)

    # Pagination for completed studies
    completed_paginator = Paginator(completed_studies, 5)
    completed_page_number = request.GET.get('completed_page')
    completed_page_obj = completed_paginator.get_page(completed_page_number)

    return render(
        request,
        'caritasapp/research_development.html',
        {
            'ongoing_page_obj': ongoing_page_obj,
            'completed_page_obj': completed_page_obj,
        }
    )
    
def interventional(request):
    department_name = 'Interventional Radiology, Radio Diagnosis and Imaging'
    department = Department.objects.get(name=department_name)
    cancer = Category.objects.get(title='cancer')
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all() 
    posts = Post.objects.filter(department__name="Interventional Radiology, Radio Diagnosis and Imaging")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/interventional.html', context)
    
def geriatric_medicine(request):
    department_name = 'Geriatric Medicine'
    department = Department.objects.get(name=department_name)
    doctors = Doctor.objects.order_by('order')
    departments = Department.objects.all()
    posts = Post.objects.filter(department__name="Geriatric Medicine")[:5]
    doctors_in_department = Doctor.objects.filter(department=department)
    context = {
        
        'posts': posts,
        'doctors_in_department': doctors_in_department,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, 'caritasapp/geriatric_medicine.html', context)

def caritashospitaldoctor_detail(request, doctor_id):
    print("View called with doctor_id:", doctor_id)
    doctor = get_object_or_404(CaritasHospitalDoctor, id=doctor_id)
    department = Department.objects.all()
    return render(request, 'caritasapp/caritashospitaldoctor_detail.html', {'doctor': doctor, 'department': department})
    
def success(request):
    return render(request, 'caritasapp/success.html')
    
#def google046804b37e953e57(request):
 #   return render(request, 'google046804b37e953e57.html')
    
def video_gallery(request):
    video_gallery = VideoGallery.objects.all().order_by('-created_at')
    return render(request, 'caritasapp/video_gallery.html', {'video_gallery' : video_gallery})
