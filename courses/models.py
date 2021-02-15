from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, blank=True)
    phone = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, blank=True)
    phone = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.username


class Department(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return str(self.name)


class Courses(models.Model):
    Instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=False, choices=[('online', 'ONLINE'), ('remote', 'REMOTE')])
    start_date = models.DateField(default=timezone.now, blank=True, null=True)
    end_date = models.DateField(default=timezone.now, blank=True, null=True)
    seat_limit = models.CharField(blank=True, max_length=20)
    seat_enrolled = models.CharField(blank=True, max_length=20)
    seat_available = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.course_name


class Enrollment(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
