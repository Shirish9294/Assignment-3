from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView
from ..forms import *
from ..models import *
from django.contrib.auth.forms import PasswordChangeForm


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('signup:signup')


class student_home(ListView):
    model = Student
    template_name = 'student/student.html'


def student_details(request):
    current_user = request.user
    student = Student.objects.get(user_id=current_user.id)
    return render(request, 'student/account.html', {'student': student})


def student_edit(request):
    # user = User
    # student = Student
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        student_form = StudentForm(request.POST, instance=request.user.student)
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            current_user = request.user
            student = Student.objects.get(user_id=current_user.id)
            return render(request, 'student/account.html', {'student': student})
    else:
        user_form = UserForm(instance=request.user)
        student_form = StudentForm(instance=request.user.student)
    return render(request, 'student/account_edit.html', {'user_form': user_form, 'student_form': student_form})


def course_list(request):
    course = Courses.objects.filter(created_date__lte=timezone.now())
    return render(request, 'student/course_list.html', {'courses': course})


def course_detail(request, pk):
    model = Courses
    course = get_object_or_404(Courses, pk=pk)
    return render(request, 'student/course_detail.html', {'courses': course})


# def enroll(request, pk):
#     form = EnrollForm(request.POST)
#     if form.is_valid():
#         enrollment = form.save(commit=False)
#         course = get_object_or_404(Courses, pk=pk)
#         enrollment.Courses = course
#         student = Student.objects.get(user=request.user)
#         enrollment.Student = student
#         if Enrollment.objects.filter(Student=student):
#             if Enrollment.objects.filter(Courses=course):
#                 return render(request, 'student/already_enrolled.html', {'courses': course})
#             else:
#                 enrollment.save()
#                 return render(request, 'student/enroll.html', {'courses': course})
#         else:
#             enrollment.save()
#             return render(request, 'student/enroll.html', {'courses': course})

def enroll(request, pk):
    form = EnrollForm(request.POST)
    if form.is_valid():
        enrollment = form.save(commit=False)
        course = get_object_or_404(Courses, pk=pk)
        enrollment.Courses = course
        student = Student.objects.get(user=request.user)
        enrollment.Student = student
        if Enrollment.objects.filter(Student=student, Courses=course).exists():
            return render(request, 'student/already_enrolled.html', {'courses': course})
        else:
            enrollment.save()
            return render(request, 'student/enroll.html', {'courses': course})


# def enrolled(request):
#     current_user = request.user
#     courses = Enrollment.objects.filter(Student=current_user.id)
#     return render(request, 'student/enrolled.html', {'courses': courses})

def enrolled(request):
    current_user = request.user
    courses = Enrollment.objects.filter(Student=current_user.id)
    return render(request, 'student/enrolled.html', {'courses': courses})


# def enrolled_class_details(request, course_name):
def enrolled_class_details(request, pk):
    str1 = get_object_or_404(Enrollment, pk=pk)
    str2 = str1.Courses
    course = get_object_or_404(Courses, course_name=str2)
    return render(request, 'student/course_detail.html', {'courses': course})


def enroll_drop(request, pk):
    drop = get_object_or_404(Enrollment, pk=pk)
    drop.delete()
    return redirect('student:enrolled')


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        course = Courses.objects.filter(course_name__contains=searched)
        return render(request, 'student/course_list.html', {'courses': course})
    else:
        return redirect('student:course_list')
