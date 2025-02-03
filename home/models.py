from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    aadhar_number = models.CharField(max_length=12, unique=True)
    date_of_birth = models.DateField(null=True)
    mother_name = models.CharField(max_length=255, null=True)
    father_name = models.CharField(max_length=255, null=True)
    marksheet_10th = models.FileField(upload_to='marksheets/10th/', null=True)
    marksheet_12th = models.FileField(upload_to='marksheets/12th/', null=True)
    college_marksheet = models.FileField(upload_to='marksheets/college/', null=True)
    aadhar_upload = models.FileField(upload_to='aadhar/', null=True)

    # Fix related_name conflicts
    groups = models.ManyToManyField(
        "auth.Group", related_name="custom_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions", blank=True
    )

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_date = models.DateField()
    documents_required = models.TextField()
    other_requirements = models.TextField(blank=True, null=True)
    poster = models.ImageField(upload_to='scholarship_posters/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
