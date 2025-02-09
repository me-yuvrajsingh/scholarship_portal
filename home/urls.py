from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('register', register_user, name='register_user'),
    path('about', about, name='about'),
    path('platform',platform , name='platform'),
    path('categories', categories, name='categories'),
    path('guide',guide, name='guide'),
    path('testimonals',testimonals, name='testimonals'),
    path('my-uploaded-scholarships',myUploadedScholarships, name='testimonals'),

    path('login/', login_user, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('post-scholarship/', uploadScholarship, name='uploadscholarship'),
    path('scholarship/<int:scholarship_id>/', scholarship_details, name='scholarship_details'),
    path('category/<str:category>/', scholarships_by_category, name='scholarships_by_category'),
    path('api/post-scholarship/', post_scholarship, name='post_scholarship'),
    path('api/categories/', category_suggestions, name='category_suggestions'),
    path('scholarship/<int:scholarship_id>/apply/', apply_scholarship, name='apply_scholarship'),
    path('scholarship/<int:scholarship_id>/applications/', view_applications, name='view_applications'),
    path('application/<int:application_id>/update/', update_application_status, name='update_application_status'),
    path('user/applications/', user_applications, name='user_applications'),
    path('my-scholarships/', user_applied_scholarships, name='my_scholarships'),
    path("get-categories/", get_categories, name="get_categories"),
] 