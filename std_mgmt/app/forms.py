from django import forms
from .models import Profile,Student

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','roll_number','department','year_of_admission']
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'email', 'department', 'year_of_admission', 'date_of_birth',]