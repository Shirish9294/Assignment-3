from django.conf.urls import url
from django.urls import path, include
from .views import courses, instructor, student
from django.contrib.auth import views as auth_views
from courses.views import *

urlpatterns = [
    path('', courses.home, name='home'),
    path('signup', courses.signup, name='signup'),
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name='password_reset'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/reset_email_sent.html"),
         name='reset_email_sent'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/reset_confirm.html"),
         name='reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/reset_complete.html"),
         name='reset_complete'),

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
                                     path('password_change/',
                                          auth_views.PasswordChangeView.as_view(
                                              template_name="registration/password_change.html"),
                                          name='password_change'),
                                     path('accounts/password_change/done/',
                                          auth_views.PasswordChangeDoneView.as_view(
                                              template_name="registration/password_change_done.html"),
                                          name='password_changed'),
                                     path('Course_new/', instructor.course_new, name='course_new'),
                                     path('Course_list/', instructor.course_list, name='course_list'),
                                     path('Course_list/<int:pk>/detail/', instructor.course_detail,
                                          name='course_detail'),
                                     path('Course_list/<int:pk>/edit/', instructor.course_edit, name='course_edit'),
                                     path('Course_list/<int:pk>/delete/', instructor.course_delete, name='course_delete'),
                                     path('Course_list/search/', instructor.search, name='search'),
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
                                           template_name="registration/password_change_done.html"),
                                       name='password_changed'),
                                  path('Course_list/', student.course_list, name='course_list'),
                                  path('Course_list/<int:pk>/detail/', student.course_detail,
                                       name='course_detail'),
                                  path('Course_list/<int:pk>/enroll/', student.enroll,
                                       name='enroll'),
                                  path('enroll_list', student.enrolled,
                                       name='enrolled'),
                                  path('enroll_list/<int:pk>/enroll_course_detail', student.enrolled_class_details,
                                       name='enrolled_class_details'),
                                  path('enroll_list/<int:pk>/drop_course', student.enroll_drop,
                                       name='enroll_drop'),
                                  path('Course_list/search/', student.search, name='search'),
                              ], 'courses'), namespace='student')),
]
