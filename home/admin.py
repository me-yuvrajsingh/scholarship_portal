from django.contrib import admin
from .models import CustomUser, Scholarship, Category

admin.site.register(CustomUser)
admin.site.register(Scholarship)
admin.site.register(Category)
