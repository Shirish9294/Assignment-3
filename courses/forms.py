from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms.widgets import DateInput
from courses.models import *


class InstructorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_instructor = True
        user.save()
        Instructor.objects.create(user=user)
        return user


class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('address', 'city', 'state', 'zipcode', 'phone')


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ('address', 'city', 'state', 'zipcode', 'phone')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ('course_name', 'department', 'description', 'location', 'start_date', 'end_date')
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


class EnrollForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ()
