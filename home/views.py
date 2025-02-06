from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser
from django.core.exceptions import ValidationError
from home.models import Scholarship, Category
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

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
        login(request, user)

        return redirect('/')

    return JsonResponse({'error': 'Invalid request'}, status=400)

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def logoutUser(request):
    logout(request)
    return redirect("/")

def uploadScholarship(request):
    return render(request, "post-scholarships.html")

def category_suggestions(request):
    query = request.GET.get('query', '')
    categories = Scholarship.objects.values_list('category', flat=True).distinct()
    suggestions = [cat for cat in categories if query.lower() in cat.lower()]
    return JsonResponse(list(suggestions), safe=False)

@csrf_exempt
def post_scholarship(request):
    if request.method == 'POST':
        try:
            data = request.POST
            files = request.FILES

            print("Received Data:", data)  # Debugging
            print("Received Files:", files)  # Debugging

            category_name = request.POST.get('category')
            try:
                category = Category.objects.get(name=category_name)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Category does not exist'}, status=400)

            required_fields = ['title', 'posted_by', 'category', 'amount', 'last_date', 'documents_required']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

            if not data['posted_by'].isdigit():  # Ensure posted_by is a valid number
                return JsonResponse({'error': 'Invalid posted_by user ID'}, status=400)

            user = User.objects.filter(id=int(data['posted_by'])).first()
            if not user:
                return JsonResponse({'error': 'User does not exist'}, status=400)

            scholarship = Scholarship(
                title=data['title'],
                posted_by=user,
                category=category,
                amount=float(data['amount']),  # Convert amount to float
                last_date=data['last_date'],
                documents_required=data['documents_required'],
                other_requirements=data.get('other_requirements', ''),
                poster=files.get('poster') if 'poster' in files else None
            )

            scholarship.full_clean()  # Validate model fields
            scholarship.save()
            return JsonResponse({'success': 'Scholarship posted successfully', 'scholarship_id': scholarship.id})
        
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            print("Unexpected Error:", e)  # Debugging
            return JsonResponse({'error': 'An unexpected error occurred'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def scholarship_details(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    return render(request, 'scholarship-details.html', {'scholarship': scholarship})

def scholarships_by_category(request, category):
    if category.lower() == "all":
        scholarships = Scholarship.objects.all().order_by('-created_at')
    else:
        category_obj = get_object_or_404(Category, name__iexact=category)
        scholarships = Scholarship.objects.filter(category=category_obj).order_by('-created_at')


    if not scholarships.exists():
        return JsonResponse({'error': 'No scholarships found for this category'}, status=404)

    data = [
        {
            'id': scholarship.id,
            'title': scholarship.title,
            'posted_by': scholarship.posted_by.username,
            'amount': float(scholarship.amount),  # Convert DecimalField to float
            'last_date': scholarship.last_date.strftime('%Y-%m-%d'),  # Convert DateField to string
            'category': scholarship.category.name,  # Get category name as a string
            'documents_required': scholarship.documents_required,
            'other_requirements': scholarship.other_requirements,
            'poster': scholarship.poster.url if scholarship.poster else None
        }
        for scholarship in scholarships
    ]
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'scholarships': data}, safe=False)
    
    return render(request, 'category.html', {"scholarships": data, "title": category})