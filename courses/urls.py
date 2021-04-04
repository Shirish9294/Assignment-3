from django.conf.urls import url
from django.urls import path, include
from .views import courses, instructor, student
from django.contrib.auth import views as auth_views
from courses.views import *

urlpatterns = [
    path('', courses.home, name='home'),

    path('signup/', include(([
                           path('', courses.SignUpView.as_view(), name='signup'),
                           path('Instructorsignup/', instructor.InstructorSignUpView.as_view(),
                                name='instructor_signup'),
                           path('studentsignup/', student.StudentSignUpView.as_view(),
                                name='student_signup'),
                       ], 'courses'), namespace='signup')),

    path('Instructor/', include(([
                                     path('', instructor.instructor_home.as_view(), name='instructor_home'),
                                     path('account', instructor.instructor_details, name='instructor_details'),
                                     path('account/edit/', instructor.instructor_edit, name='instructor_edit'),
                                     path('account/password_change/',
                                          auth_views.PasswordChangeView.as_view(
                                              template_name="registration/password_change.html"),
                                          name='password_change'),
                                     path('account/password_change/done/',
                                          auth_views.PasswordChangeDoneView.as_view(
                                              template_name="registration/password_changed.html"),
                                          name='password_changed'),
                                 ], 'courses'), namespace='instructor')),

    path('Student/', include(([
                                  path('', student.student_home.as_view(), name='student_home'),
                                  path('account', student.student_details, name='student_details'),
                                  path('account/edit/', student.student_edit, name='student_edit'),
                                  path('account/password_change/',
                                       auth_views.PasswordChangeView.as_view(
                                           template_name="registration/password_change.html"),
                                       name='password_change'),
                                  path('account/password_change/done/',
                                       auth_views.PasswordChangeDoneView.as_view(
                                           template_name="registration/password_changed.html"),
                                       name='password_changed'),
                              ], 'courses'), namespace='student')),
]
