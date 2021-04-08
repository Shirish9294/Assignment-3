from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView
from ..forms import *
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


def course_new(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_date = timezone.now()
            instructor = Instructor.objects.get(user=request.user)
            course.instructor = instructor
            course.save()
            courses = Courses.objects.filter(created_date__lte=timezone.now())
            return render(request, 'instructor/added_successful.html', {'courses': courses})

    else:
        form = CourseForm()
    return render(request, 'instructor/course_new.html', {'form': form})


def course_list(request):
    instructor = Instructor.objects.get(user=request.user)
    course = Courses.objects.filter(created_date__lte=timezone.now(), instructor=instructor)
    return render(request, 'instructor/course_list.html', {'courses': course})


def course_detail(request, pk):
    model = Courses
    course = get_object_or_404(Courses, pk=pk)
    return render(request, 'instructor/course_detail.html', {'courses': course})


def course_edit(request, pk):
    course = get_object_or_404(Courses, pk=pk)
    if request.method == "POST":
        # update
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.updated_date = timezone.now()
            course.save()
            courses = Courses.objects.filter(created_date__lte=timezone.now())
            # return render(request, 'instructor/course_list.html',
            #               {'courses': courses})
            return redirect('instructor:course_list')
    else:
        # edit
        form = CourseForm(instance=course)
    return render(request, 'instructor/course_edit.html', {'form': form})


def course_delete(request, pk):
    course = get_object_or_404(Courses, pk=pk)
    course.delete()
    return redirect('instructor:course_list')


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        instructor = Instructor.objects.get(user=request.user)
        course = Courses.objects.filter(instructor=instructor, course_name__contains=searched)
        return render(request, 'instructor/course_list.html', {'courses': course})
    else:
        return redirect('instructor:course_list')
