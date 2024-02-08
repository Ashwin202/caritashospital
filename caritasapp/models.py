from django.db import models
from django.utils.html import mark_safe
from moviepy.video.io.VideoFileClip import VideoFileClip
from django.core.files.base import ContentFile
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from django.dispatch import receiver
from django.db.models.signals import post_save
import tempfile
from django.utils.text import Truncator
from django.db.models.signals import pre_save
from django.urls import reverse
import uuid

class Department(models.Model):
    name = models.CharField(max_length=100)
    Department_id =  models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    slug = models.SlugField()
    Department_url = models.TextField(null=True, blank=True)
    #Department_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name
        
class Category(models.Model):
    title = models.CharField(max_length=100)
    Category_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    slug = models.SlugField()

    def __str__(self):
        return self.title

def get_default_category():
    # Retrieve the default category object (for example, the first category object in the database)
    return Category.objects.first()
    
class Subcategory(models.Model):
    subcat_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # Add a slug field if needed

    # Add any other fields you need for your Subcategory model

    def __str__(self):
        return self.subcat_title

        
def get_default_subcategory():
    return Subcategory.objects.first()
        
class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')
    body = models.TextField()
    post_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', default=get_default_category)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True)
    excerpt = models.TextField(blank=True)  # Allow it to be blank if you want to manually set excerpts

    def save(self, *args, **kwargs):
        # Generate excerpt from body if not provided manually
        if not self.excerpt:
            self.excerpt = Truncator(self.body).chars(200)  # Truncate to 200 characters
        super(Post, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Post)
def set_default_category(sender, instance, **kwargs):
    # Set the default category if category is not provided
    if instance.category is None:
        instance.category = get_default_category()
        
class Card(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/card_images/')

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='videos/', default='default_video.mp4')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.thumbnail:
            try:
                # Create a temporary file for the thumbnail
                with tempfile.NamedTemporaryFile(delete=True) as temp_thumbnail:
                    clip = VideoFileClip(self.file.path)
                    frame = clip.get_frame(1)  # Get the frame at the 1-second mark
                    frame.save(temp_thumbnail.name, format='JPEG')

                    # Save the thumbnail to the 'thumbnail' field
                    self.thumbnail.save(f"{self.title}_thumbnail.jpg", ContentFile(temp_thumbnail.read()), save=True)

            except Exception as e:
                # Handle any exceptions that might occur during thumbnail generation
                pass

class Enquire(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    page_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'
        
        
class ContactUs(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    page_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

#class Doctor(models.Model):
  #  name = models.CharField(max_length=100)
   # Doctor_id =  models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  #  slug = models.SlugField()
    #body = models.TextField()
   # position = models.CharField(max_length=255)
  #  department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True)
  #  speciality = models.ForeignKey('Speciality', on_delete=models.SET_NULL, blank=True, null=True)
  #  def __str__(self):
  #      return self.name
        

        
class Speciality(models.Model):
    name = models.CharField(max_length=100)
    Speciality_id =  models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    slug = models.SlugField()
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.name
class Hospital(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        
class Doctor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None) 
    designation = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255,blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    professional_qualifications = models.CharField(max_length=1000, blank=True)
    achievements_and_expertise = models.TextField(blank=True)
    awards_and_recognitions = models.TextField(blank=True)
    language = models.CharField(max_length=255, blank=True)
    hospitals = models.ManyToManyField(Hospital, blank=True)
    order=  models.CharField(max_length=255, blank=True)
    is_visible = models.BooleanField(default=True)
    appointment_enabled = models.BooleanField(default=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if an image is provided
        if not self.image:
            # If no image is provided, you can set a default image path or leave it blank
            self.image = 'doctors/Default.png'  # Change this to your default image path

        super().save(*args, **kwargs)
        
        
class Contact(models.Model):
    QUERY_CHOICES = (
        ('Enquiry', 'Enquiry'),
        ('Complaint', 'Complaint'),
        ('Feedback', 'Feedback'),
    )

    query_type = models.CharField(max_length=20, choices=QUERY_CHOICES)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, default='Rheumatology')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class JobType(models.Model):
    job_type = models.CharField(max_length=100)
    job_type_id =  models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    slug = models.SlugField()
    def __str__(self):
        return self.job_type     

class Career(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    job_title = models.CharField(max_length=255)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, null=True, blank=True)
    department = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    job_discription = models.TextField(blank=True)
    key_responsibilities = models.TextField(blank=True)
    preferred_skills = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
  
class Application(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    job_title = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    agree_terms = models.BooleanField()
    page_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_title}"
        
from django.db import models

class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    caption = models.CharField(max_length=100)
    title = models.CharField(max_length=620, blank=True)
    description = models.TextField(blank=True)
    category=models.CharField(max_length=100, blank=True)
    # Add other fields if needed

    def __str__(self):
        return self.caption 
        
class MobileSliderImage(models.Model):
    image = models.ImageField(upload_to='mobileslider_images/')
    caption = models.CharField(max_length=100)
    title = models.CharField(max_length=620, blank=True)
    description = models.TextField(blank=True)
    category=models.CharField(max_length=100, blank=True)
    # Add other fields if needed

    def __str__(self):
        return self.caption  # Or any other field you want to represent in admin
        
class Videos(models.Model):
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=20)  # Store YouTube video IDs

    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=100)

class Image(models.Model):
    album = models.ForeignKey(Album, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True)

class QualityControl(models.Model):
    average_length=models.CharField(max_length=100)
    patient_satisfaction=models.CharField(max_length=100)
    cauti=models.CharField(max_length=100)
    vap=models.CharField(max_length=100)
    clabsi=models.CharField(max_length=100)
    ssi=models.CharField(max_length=100)
    pressure_ulcers_afteradmission=models.CharField(max_length=100)
    compliance_hand_hygiene=models.CharField(max_length=100)
    month_year = models.DateField(verbose_name="Month and Year", null=True, blank=True)

    def formatted_date(self):
        return self.month_year.strftime("%d-%b-%y") if self.month_year else ''

    def __str__(self):
        return f"QualityControl for {self.formatted_date()}"
        
class BioMedical(models.Model):
    total_bags=models.CharField(max_length=100)
    yellow_bags=models.CharField(max_length=100)
    red_bags=models.CharField(max_length=100)
    white_bags=models.CharField(max_length=100)
    brownish_yellow_bags=models.CharField(max_length=100)
    blue_bags=models.CharField(max_length=100)
    
    month_year = models.DateField(verbose_name="Month and Year", null=True, blank=True)

    def __str__(self):
        return f"BioMedical for {self.month_year}"
        
class Studies(models.Model):
    study_name=models.TextField(blank=True)
    investigators=models.CharField(max_length=100)
    category=models.CharField(max_length=100,null=True, blank=True)
    
    
class HomeCare(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'
        
class BookConsultation(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)
    dob = models.DateField(blank=True, null=True)
    op_number = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,blank=True, null=True)
    message = models.TextField(blank=True)
    agree_terms = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
class InternationalForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
class CaritasHospitalDoctor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None) 
    designation = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255,blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    professional_qualifications = models.CharField(max_length=1000, blank=True)
    achievements_and_expertise = models.CharField(max_length=1000, blank=True)
    awards_and_recognitions = models.CharField(max_length=1000, blank=True)
    language = models.CharField(max_length=255, blank=True)
    hospitals = models.ManyToManyField(Hospital, blank=True)
    order=  models.CharField(max_length=255, blank=True)
    is_visible = models.BooleanField(default=True)
   
    available_timings = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
        
class DoctorSlider(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='doctors_images/')
    
