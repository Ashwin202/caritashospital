from django import forms
from .models import Enquire
from .models import Department , Doctor, Contact,ContactUs,Application, HomeCare,InternationalForm,BookConsultation
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os

class EnquireForm(forms.ModelForm):
    class Meta:
        model = Enquire
        fields = ['first_name', 'last_name', 'email', 'phone_number'] 
        
    

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['query_type', 'name', 'email', 'department', 'doctor', 'message']
    
class DoctorSearchForm(forms.Form):
    query = forms.CharField(label='Search Doctors', max_length=100, required=False)
    
class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'email', 'phone_number'] 
        
class HomeCareForm(forms.ModelForm):
    class Meta:
        model = HomeCare
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'package'] 


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'resume', 'agree_terms']
        widgets = {
            'agree_terms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
   
        }


class DepartmentFilterForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department')

class InternationalForm(forms.ModelForm):
    class Meta:
        model = InternationalForm
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or not first_name.strip().isalpha():
            raise forms.ValidationError("Please enter a valid first name.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or not last_name.strip().isalpha():
            raise forms.ValidationError("Please enter a valid last name.")
        return last_name
        
class BookConsultationForm(forms.ModelForm):
    class Meta:
        model = BookConsultation
        fields = ['first_name', 'last_name', 'gender', 'email', 'country', 'phone_number', 'dob', 'op_number', 'department', 'doctor', 'message', 'agree_terms']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookConsultationForm, self).__init__(*args, **kwargs)
        