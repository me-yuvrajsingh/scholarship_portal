from django.contrib import admin
from .models import CustomUser, Scholarship, Category, ScholarshipApplication

admin.site.register(CustomUser)
admin.site.register(Scholarship)
admin.site.register(Category)
admin.site.register(ScholarshipApplication)
