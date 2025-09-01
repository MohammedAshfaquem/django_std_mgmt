from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProfileForm,StudentForm
from .models import Profile,Student
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator




def Register(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm()
    return render(request,'register.html',{'form':form})


def Login(request):
    if request.method == "POST":
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')

        try:
            user = Profile.objects.get(roll_number=roll_number)
            if user.name == name:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                messages.error(request, "Invalid name for this roll number.")
        except Profile.DoesNotExist:
            messages.error(request, "Invalid user. Please check your roll number.")

        return redirect('login')

    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('login')


def home_view(request):
    return render(request,'base.html',)


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

    paginator = Paginator(students, 5,orphans=1)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {
        'students': page_obj,
        'page_obj': page_obj,
    })



    
def student_create(request):
    user_id = request.session.get('user_id')
    current_user = get_object_or_404(Profile, id=user_id)

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.profile = current_user
            student.save()
            messages.success(request, "Student added successfully!")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_create.html', {'form': form})


def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_edit.html', {'form': form})



def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")
    return render(request, "student_delete.html", {"student": student})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student_detail.html', {'student': student})
# Create your views here.
