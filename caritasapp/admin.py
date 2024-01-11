from django.contrib import admin
from .models import Post, Category,Subcategory, Video, Department,Speciality, Doctor, Contact, ContactUs, Career, JobType,Application,SliderImage,Videos,Album, Image, MobileSliderImage, QualityControl, Studies,BioMedical,HomeCare, Hospital,InternationalForm
from .models import Enquire

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
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'page_url', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'page_url')
    readonly_fields = ('created_at',)
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number',  'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    readonly_fields = ('created_at',)
    
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
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'job_title', 'resume','created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'job_title')
    list_filter = ('created_at',)
    
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image')
    
class MobileSliderImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image')

class VideosAdmin(admin.ModelAdmin):
    list_display = ('title',)
    

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3  # Number of empty slots for uploading images

class AlbumAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    
class QualityControlAdmin(admin.ModelAdmin):
    list_display =('average_length','patient_satisfaction','cauti','vap','clabsi','ssi','pressure_ulcers_afteradmission','compliance_hand_hygiene', 'month_year')
    list_filter = ('month_year',) 
    
class BioMedicalAdmin(admin.ModelAdmin):
    list_display = ('total_bags','yellow_bags','red_bags','white_bags','brownish_yellow_bags','blue_bags')
    list_filter = ('month_year',) 

class StudiesAdmin(admin.ModelAdmin):
    list_display = ('study_name','investigators')
    list_filter =('study_name','investigators')
class HomeCareAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'message',  'created_at')
    search_fields = ('first_name', 'last_name', 'email',)
    list_filter =('first_name', 'last_name', 'email',)
    readonly_fields = ('created_at',)
    
class InternationalFormAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'country']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'country']
    
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
admin.site.register(Application, ApplicationAdmin) 
admin.site.register(SliderImage,SliderImageAdmin)
admin.site.register(MobileSliderImage,MobileSliderImageAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(QualityControl,QualityControlAdmin)
admin.site.register(BioMedical,BioMedicalAdmin)
admin.site.register(Studies,StudiesAdmin)
admin.site.register(HomeCare, HomeCareAdmin)
admin.site.register(Hospital,HospitalAdmin)
admin.register(InternationalForm,InternationalFormAdmin)