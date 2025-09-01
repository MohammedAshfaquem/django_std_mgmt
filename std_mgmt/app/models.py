from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    name = models.CharField(max_length=30,null=False, blank=False)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('student', 'Student')])
    roll_number = models.CharField(max_length=20, null=False, blank=False,unique=True)
    department = models.CharField(max_length=50, null=False, blank=False)
    year_of_admission = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name
    


class Student(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="students")
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20,unique=True)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    year_of_admission = models.IntegerField()
    date_of_birth = models.DateField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


# Create your models here.
