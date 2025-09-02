from django.urls import path
from . import views
urlpatterns = [
    path('',views.home_view,name='home'),
    path('register/',views.Register,name='register'),
    path('login/',views.Login,name='login'),
    path('logout/', views.logout, name='logout'),
    path("profile/", views.profile_view, name="profile_view"),
    path("profile/edit/<int:pk>/", views.profile_edit, name="profile_edit"),
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
]