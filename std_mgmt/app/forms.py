from django import forms
from .models import Profile,Student

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'roll_number', 'department', 'year_of_admission', 'role']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Name'
            }),
            'roll_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Roll Number'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Department'
            }),
            'year_of_admission': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Admission Year'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            })
        }

        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'roll_number',
            'email',
            'department',
            'year_of_admission',
            'date_of_birth',
            'profile_pic'
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter student name"
            }),
            "roll_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter roll number"
            }),
           "department": forms.TextInput(attrs={
           "class": "form-control",
           "placeholder": "Enter department",
           "list": "department-options"
            }),
            "year_of_admission": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "2025"
            }),
            "date_of_birth": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email"
            }),
            "profile_pic": forms.FileInput(attrs={
                "class": "form-control"
            }),
        }
