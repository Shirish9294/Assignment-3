from django.contrib import admin
from courses.models import User, Student, Instructor, Enrollment, Courses
# Register your models here.
admin.site.register(User)

admin.site.register(Instructor)

# admin.site.register(Department)

admin.site.register(Courses)

admin.site.register(Student)

admin.site.register(Enrollment)

