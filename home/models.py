from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    aadhar_number = models.CharField(max_length=12, unique=True)
    date_of_birth = models.DateField()
    mother_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    marksheet_10th = models.FileField(upload_to='marksheets/10th/')
    marksheet_12th = models.FileField(upload_to='marksheets/12th/')
    college_marksheet = models.FileField(upload_to='marksheets/college/')
    aadhar_upload = models.FileField(upload_to='aadhar/')

    # Fix related_name conflicts
    groups = models.ManyToManyField(
        "auth.Group", related_name="custom_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions", blank=True
    )

    def __str__(self):
        return self.username
