from django.urls import path
from .views import *

urlpatterns = [
    path("", home , name="home"),
    path("<pk>", student_data , name="student-data"),
    path("logout/",logout_user, name="logout-user"),
    path("update_data/",update_student, name="update-user"),
    path("edit-details/<pk>/<data>", update_data , name="update-user"),
    path("login/" , login_user , name = "login-user"),
    path("signup/", signup, name="register-user")
]
