from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, ScholarshipApplication
from django.core.exceptions import ValidationError
from home.models import Scholarship, Category
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

User = get_user_model()

def home(request):
    scholarships = Scholarship.objects.all().order_by('-created_at')[:9]
    return render(request, "index.html", {'scholarships': scholarships})

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

        full_name = request.POST.get("name", "").strip()
        name_parts = full_name.split()
        first_name = name_parts[0] if name_parts else "Unknown"
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        # Validate password match
        if data['password'] != data.get('confirm_password'):
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        # Check if user already exists
        if CustomUser.objects.filter(username=data['email']).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)

        # Create the user
        user = CustomUser(
            username=data['email'],
            first_name=first_name,
            last_name=last_name,
            email=data['email'],
            phone_number=data['phone_number'],
            aadhar_number=request.POST.get("aadhar_number", ""),
            gst_number=request.POST.get("gst_number", ""),
            acc_type=data['acc_type'],
            date_of_birth=request.POST.get("date_of_birth", None),
            mother_name=request.POST.get("mother_name", ""),
            father_name=request.POST.get("father_name", ""),
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

            user = CustomUser.objects.filter(id=int(data['posted_by'])).first()
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
    user_application = ScholarshipApplication.objects.filter(scholarship=scholarship, applicant=request.user).first()
    return render(request, 'scholarship-details.html', {'scholarship': scholarship, "user_application": user_application})

def scholarships_by_category(request, category):
    if category.lower() == "all":
        scholarships = Scholarship.objects.all().order_by('-created_at')
    else:
        category_obj = get_object_or_404(Category, name__iexact=category)
        scholarships = Scholarship.objects.filter(category=category_obj).order_by('-created_at')


    # if not scholarships.exists():
    #     return JsonResponse({'error': 'No scholarships found for this category'}, status=404)

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

@login_required
def apply_scholarship(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)

    if request.method == "POST":
        reason = request.POST.get("reason")
        application, created = ScholarshipApplication.objects.get_or_create(
            scholarship=scholarship,
            applicant=request.user,
            defaults={"reason": reason}
        )
        
        if not created:
            return JsonResponse({"error": "You have already applied for this scholarship"}, status=400)

        return JsonResponse({"success": "Application submitted successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def view_applications(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id, posted_by=request.user)
    applications = ScholarshipApplication.objects.filter(scholarship=scholarship)

    return render(request, "view_applications.html", {"scholarship": scholarship, "applications": applications})

@login_required
def update_application_status(request, application_id):
    if request.method == "POST":
        application = get_object_or_404(ScholarshipApplication, id=application_id, scholarship__posted_by=request.user)
        status = request.POST.get("status")

        if status not in dict(ScholarshipApplication.STATUS_CHOICES):
            return JsonResponse({"error": "Invalid status"}, status=400)

        application.status = status
        application.save()
        return JsonResponse({"success": "Application status updated successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def user_applications(request):
    applications = ScholarshipApplication.objects.filter(applicant=request.user)
    return render(request, "user_applications.html", {"applications": applications})

@login_required
def user_applied_scholarships(request):
    """ View scholarships the user has applied for """
    applied_scholarships = ScholarshipApplication.objects.filter(applicant=request.user)

    return render(request, "applied_scholarships.html", {
        "applied_scholarships": applied_scholarships
    })

def get_categories(request):
    """ Fetch all available categories and return as JSON """
    categories = Category.objects.values("id", "name")
    return JsonResponse({"categories": list(categories)})