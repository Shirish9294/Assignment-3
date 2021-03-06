from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_instructor:
            return redirect('instructor:instructor_home')
        elif request.user.is_student:
            return redirect('student:student_home')
    return render(request, 'courses/home.html')


def signup(request):
    return render(request, 'registration/signup.html')