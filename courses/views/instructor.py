from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView
from ..forms import InstructorSignUpForm, UserForm, InstructorForm
from ..models import *

now = timezone.now()


class InstructorSignUpView(CreateView):
    model = User
    form_class = InstructorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'instructor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('signup:signup')


class instructor_home(ListView):
    model = Instructor
    template_name = 'instructor/instructor.html'


def instructor_details(request):
    current_user = request.user
    instructor = Instructor.objects.get(user_id=current_user.id)
    return render(request, 'instructor/account.html', {'instructor': instructor})


def instructor_edit(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        instructor_form = InstructorForm(request.POST, instance=request.user.instructor)
        if user_form.is_valid() and instructor_form.is_valid():
            user_form.save()
            instructor_form.save()
            current_user = request.user
            instructor = Instructor.objects.get(user_id=current_user.id)
            return render(request, 'instructor/account.html', {'instructor': instructor})
    else:
        user_form = UserForm(instance=request.user)
        instructor_form = InstructorForm(instance=request.user.instructor)
    return render(request, 'instructor/account_edit.html', {'user_form': user_form, 'instructor_form': instructor_form})
