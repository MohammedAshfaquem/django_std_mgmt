from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .forms import ProfileForm, StudentForm
from .models import Profile, Student
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
    
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        user = get_object_or_404(Profile, id=user_id)
        if user.role != 'admin':
            return redirect('student_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        user = get_object_or_404(Profile, id=user_id)
        if user.role != 'student':
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def Register(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id  
            if user.role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("student_dashboard")
    else:
        form = ProfileForm()
    return render(request, "register.html", {"form": form})

def Login(request):
    if request.method == "POST":
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        try:
            user = Profile.objects.get(roll_number=roll_number)
            if user.name == name:
                request.session['user_id'] = user.id
                request.session['user_role'] = user.role
                if user.role == "admin":
                    return redirect("admin_dashboard")
                else:
                    return redirect("student_dashboard") 
            else:
                messages.error(request, "Invalid name for this roll number.")
        except Profile.DoesNotExist:
            messages.error(request, "Invalid user. Please check your roll number.")
        return redirect('login')
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'base.html')

@login_required
@student_required
def student_dashboard(request):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Profile, id=user_id)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("student_dashboard")
    else:
        form = ProfileForm(instance=user)

    return render(request, "student_dashboard.html", {
        "user": user,
        "form": form,
    })

@login_required
def profile_view(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(Profile, id=user_id)
    return render(request, "profile.html", {"user": user})

@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_view")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profile_edit.html", {"form": form})

@admin_required
@login_required
def student_list(request):
    user_id = request.session.get('user_id')
    current_user = get_object_or_404(Profile, id=user_id)
    students = Student.objects.filter(profile=current_user)

    query = request.GET.get('q')
    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(email__icontains=query) |
            Q(department__icontains=query)
        )

    paginator = Paginator(students, 5, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {
        'students': page_obj,
        'page_obj': page_obj,
    })

@admin_required
@login_required
def student_create(request):
    user_id = request.session.get('user_id')
    current_user = get_object_or_404(Profile, id=user_id)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.profile = current_user
            student.save()
            messages.success(request, "Student added successfully!")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_create.html', {'form': form})

@admin_required
@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_edit.html', {'form': form})

@admin_required
@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")
    return render(request, "student_delete.html", {"student": student})

@admin_required
@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student_detail.html', {'student': student})


def find(request):
    if request.method == 'POST':
        result = request.POST.get('find')
        print(result)
        try:
            std = Student.objects.filter(name__contains =result)
            print(std)
            return render(request,"res.html",{"std":std})
        except:
            return HttpResponse("No User")
    return render(request,'res.html',)

