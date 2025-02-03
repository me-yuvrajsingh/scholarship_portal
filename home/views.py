from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser

def home(request):
    return render(request, "index.html")

def signup(request):
    return render(request, "signup.html")

def about(request):
    return render(request, "about.html")

def platform(request):
    return render(request, "platform.html")

def categories(request):
    return render(request, "categories.html")

def guide(request):
    return render(request, "guide.html")
    
def testimonals(request):
    return render(request, "testimonals.html")



def register_user(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        # Validate password match
        if data['password'] != data.get('confirm_password'):
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        # Validate file uploads
        if not files.get('marksheet_10th') or not files.get('marksheet_12th') or not files.get('college_marksheet') or not files.get('aadhar_upload'):
            return JsonResponse({'error': 'All files are required'}, status=400)

        # Check if user already exists
        if CustomUser.objects.filter(username=data['email']).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)

        # Create the user
        user = CustomUser(
            username=data['email'],
            email=data['email'],
            phone_number=data['phone_number'],
            aadhar_number=data['aadhar_number'],
            date_of_birth=data['date_of_birth'],
            mother_name=data['mother_name'],
            father_name=data['father_name'],
            marksheet_10th=files.get('marksheet_10th'),
            marksheet_12th=files.get('marksheet_12th'),
            college_marksheet=files.get('college_marksheet'),
            aadhar_upload=files.get('aadhar_upload'),
            password=make_password(data['password'])
        )
        user.save()

        return redirect('/')

    return JsonResponse({'error': 'Invalid request'}, status=400)