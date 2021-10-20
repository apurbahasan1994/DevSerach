from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('/projects', views.projects, name="projects"),
    path('/create_project', views.create_project, name="create_project"),
    path('/submit_project', views.submit_project, name='submit_project'),
    path('/update_project/<str:pk>/', views.update_project, name='update_project'),
    path('/delete_project/<str:pk>/', views.delete_project, name='delete_project'),
    path('/login', views.login_page, name="login"),
    path('/logout', views.logout_user, name="logout"),
    path('signup', views.signup, name="signup"),
    path('/single_project/<str:pk>/', views.single_project, name="single_project"),
    path('/user/<str:pk>', views.profile_page, name="userprofile"),
    path('/useraccount', views.useraccount, name='useraccount'),
    path('/update_profile', views.update_profile, name="update_profile"),
    path('/addskill', views.addskill, name="addskill"),
    path('/deleteskill/<str:pk>', views.deleteskill, name="deleteskill"),
    path('/editskill/<str:pk>', views.editskill, name="editskill"),
    path('/inbox', views.inbox, name='inbox'),
    path('/message/<str:pk>', views.view_message, name="message"),
    path('/sendmessage/<str:pk>', views.sendmessage, name="sendmessage"),
    path('/reset_password/', auth_views.PasswordResetView.as_view(template_name="project/reset_password.html"),
         name="reset_password"),

    path('/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="project/reset_password_sent.html"),
         name="password_reset_done"),

    path('/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="project/reset.html"),
         name="password_reset_confirm"),

    path('/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="project/reset_password_complete.html"),
         name="password_reset_complete"),

]
