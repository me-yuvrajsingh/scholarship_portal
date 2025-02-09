from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    aadhar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    gst_number = models.CharField(max_length=12, blank=True, null=True)
    acc_type = models.CharField(max_length=2, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    marksheet_10th = models.FileField(upload_to='marksheets/10th/', null=True, blank=True)
    marksheet_12th = models.FileField(upload_to='marksheets/12th/', null=True, blank=True)
    college_marksheet = models.FileField(upload_to='marksheets/college/', null=True, blank=True)
    aadhar_upload = models.FileField(upload_to='aadhar/', null=True, blank=True)

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

class ScholarshipApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.applicant.username} - {self.scholarship.title}"
