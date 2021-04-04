from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView
from ..forms import StudentSignUpForm, UserForm, StudentForm
from ..models import User, Student
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
