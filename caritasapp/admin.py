from django.contrib import admin
from .models import Post, Category,Subcategory, Video, Department,Speciality, Doctor, Contact, ContactUs, Career, JobType,Application,SliderImage,Videos,Album, Image, MobileSliderImage, QualityControl, Studies,BioMedical,HomeCare, Hospital,InternationalForm,BookConsultation,DoctorSlider, CaritasHospitalDoctor
from .models import Enquire,JobApply,CareerEnquire
from .models import VideoGallery
import csv
from django.http import HttpResponse
from django.utils.html import format_html

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category','department')  
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If a category filter is applied, filter the queryset accordingly
        category_id = request.GET.get('category__id')
        if category_id:
            return qs.filter(category__id=category_id)
        return qs

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('subcat_title',)}


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title',) 
    
class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

#class DoctorAdmin(admin.ModelAdmin):
   # prepopulated_fields = {'slug': ('name','position','body','department','speciality')}
class HospitalAdmin(admin.ModelAdmin):
    
    list_display =('name',)
    
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization','image')
    search_fields = ('name', 'specialization',)


class SpecialityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name','department')}    
    
class EnquireAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'message', 'page_url', 'created_at')
    search_fields = ('name', 'email', 'phone_number', 'page_url')
    readonly_fields = ('created_at',)

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="enquiries.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone Number', 'Message','Page URL', 'Created At'])

        for enquiry in queryset:
            writer.writerow([
                enquiry.name,
                enquiry.email,
                enquiry.phone_number,
                enquiry.message,
                enquiry.page_url,
                enquiry.created_at,
            ])

        return response

    export_as_csv.short_description = "Export selected enquiries as CSV"
    actions = ['export_as_csv']
    
class CareerEnquireAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'message', 'page_url', 'created_at')
    search_fields = ('name', 'email', 'phone_number', 'page_url')
    readonly_fields = ('created_at',)

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="enquiries.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone Number', 'Message','Page URL', 'Created At'])

        for enquiry in queryset:
            writer.writerow([
                enquiry.name,
                enquiry.email,
                enquiry.phone_number,
                enquiry.message,
                enquiry.page_url,
                enquiry.created_at,
            ])

        return response

    export_as_csv.short_description = "Export selected enquiries as CSV"
    actions = ['export_as_csv']
    
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number','message', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    readonly_fields = ('created_at',)

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contact_us.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number', 'Page URL', 'Created At'])
        for obj in queryset:
            writer.writerow([obj.first_name, obj.last_name, obj.email, obj.phone_number, obj.page_url, obj.created_at])
        return response

    export_as_csv.short_description = "Export Selected Contacts"

    actions = ['export_as_csv']  # Add the export action to the admin interface
    
class ContactAdmin(admin.ModelAdmin):
    list_display = ('query_type', 'name', 'email', 'department', 'doctor', 'created_at')
    search_fields = ('query_type', 'name', 'email', 'department__name', 'doctor__name', 'created_at')
    list_filter = ('query_type', 'created_at')
    
class JobTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('job_type',)}
    
class CareerAdmin(admin.ModelAdmin):
    list_display = ('job_title','job_type', 'department','qualification','created_at')
    search_fields = ('job_title', 'department','job_type')
    
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'job_title', 'resume', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'job_title')
    list_filter = ('created_at',)
    actions = ['export_as_csv']

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}">Download Resume</a>', obj.resume.url)
        return '-'

    resume_link.short_description = 'Resume'

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applications.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number', 'Job Title', 'Resume', 'Created At'])
        for obj in queryset:
            writer.writerow([obj.first_name, obj.last_name, obj.email, obj.phone_number, obj.job_title, obj.resume.url if obj.resume else '', obj.created_at])
        return response

    export_as_csv.short_description = "Export Selected Applications"

    
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image')
    
class MobileSliderImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image')

class VideosAdmin(admin.ModelAdmin):
    list_display = ('title','created_at')
    

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3  # Number of empty slots for uploading images

class AlbumAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    
class QualityControlAdmin(admin.ModelAdmin):
    list_display =('average_length','patient_satisfaction','cauti','vap','clabsi','ssi','pressure_ulcers_afteradmission','compliance_hand_hygiene', 'month_year')
    list_filter = ('month_year',) 
    
class BioMedicalAdmin(admin.ModelAdmin):
    list_display = ('total_bags','yellow_bags','red_bags','white_bags','brownish_yellow_bags','blue_bags','month_year')
    list_filter = ('month_year',) 

class StudiesAdmin(admin.ModelAdmin):
    list_display = ('study_name','investigators')
    list_filter =('study_name','investigators')

class HomeCareAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    readonly_fields = ('created_at',)

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="homecare_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number', 'Created At'])
        for obj in queryset:
            writer.writerow([obj.first_name, obj.last_name, obj.email, obj.phone_number, obj.created_at])
        return response

    export_as_csv.short_description = "Export Selected HomeCare Data"

    actions = [export_as_csv]

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="homecare_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Created At'])
        for obj in queryset:
            writer.writerow([obj.first_name, obj.last_name, obj.email,  obj.created_at])
        return response

    export_as_csv.short_description = "Export Selected HomeCare Data"

    actions = [export_as_csv]
    
class InternationalFormAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'message']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'country']

class InternationalAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number','country',  'created_at')
    search_fields = ('first_name', 'last_name', 'email','country',)
    list_filter =('first_name', 'last_name', 'email','country',)
    readonly_fields = ('created_at',)
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="international_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number', 'Country', 'Created At'])
        for obj in queryset:
            writer.writerow([obj.first_name, obj.last_name, obj.email, obj.phone_number, obj.country, obj.created_at])
        return response

    export_as_csv.short_description = "Export Selected International Data"
    actions = [export_as_csv]
    
class BookConsultationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'country', 'phone_number','op_number', 'gender','department','doctor','created_at']
    search_fields = ['first_name', 'last_name', 'email','gender']
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="book_consultation_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Gender', 'Email', 'Country', 'Phone Number', 'Date of Birth', 'Operation Number', 'Department', 'Doctor', 'Message', 'Agree to Terms', 'Created At'])
        for obj in queryset:
            writer.writerow([obj.first_name, obj.last_name, obj.gender, obj.email, obj.country, obj.phone_number, obj.dob, obj.op_number, obj.department, obj.doctor, obj.message, obj.agree_terms, obj.created_at])
        return response

    export_as_csv.short_description = "Export Selected Consultations"
    actions = [export_as_csv]
    
    
class CaritasHospitalDoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'image', 'display_hospitals')
    list_filter = ['name', 'specialization', 'hospitals']
    search_fields = ('name', 'specialization',)

    def display_hospitals(self, obj):
        return ", ".join([hospital.name for hospital in obj.hospitals.all()])

    display_hospitals.short_description = 'Hospitals'

class DoctorSliderAdmin(admin.ModelAdmin):
    list_display = ('title','image',)
    
class JobApplyAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'resume', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('created_at',)
    actions = ['export_as_csv']

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}">Download Resume</a>', obj.resume.url)
        return '-'

    resume_link.short_description = 'Resume'

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applications.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number', 'Resume', 'Created At'])
        for obj in queryset:
            writer.writerow([obj.first_name, obj.last_name, obj.email, obj.phone_number, obj.resume.url if obj.resume else '', obj.created_at])
        return response

    export_as_csv.short_description = "Export Selected Applications"
    
class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')    
    
admin.site.register(Album, AlbumAdmin)

    
admin.site.register(Contact, ContactAdmin)    

admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(JobType, JobTypeAdmin)
admin.site.register(Career, CareerAdmin) 
admin.site.register(Category, CategoryAdmin)   
admin.site.register(Subcategory, SubcategoryAdmin)   
admin.site.register(Post, PostAdmin)

admin.site.register(Video, VideoAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Enquire, EnquireAdmin)
admin.site.register(CareerEnquire, CareerEnquireAdmin)
admin.site.register(Application, ApplicationAdmin) 
admin.site.register(SliderImage,SliderImageAdmin)
admin.site.register(MobileSliderImage,MobileSliderImageAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(QualityControl,QualityControlAdmin)
admin.site.register(BioMedical,BioMedicalAdmin)
admin.site.register(Studies,StudiesAdmin)
admin.site.register(HomeCare, HomeCareAdmin)
admin.site.register(Hospital,HospitalAdmin)
#admin.register(InternationalForm,InternationalFormAdmin)
admin.site.register(InternationalForm, InternationalAdmin)
admin.site.register(BookConsultation, BookConsultationAdmin)
admin.site.register(VideoGallery, VideoGalleryAdmin)
admin.site.register(CaritasHospitalDoctor, CaritasHospitalDoctorAdmin)
admin.site.register(DoctorSlider,DoctorSliderAdmin)
admin.site.register(JobApply,JobApplyAdmin)