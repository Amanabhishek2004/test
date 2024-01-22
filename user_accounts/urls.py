from django.urls import path
from .views import *

urlpatterns = [
    path("", home , name="home"),
    path("edit/<pk>", edit_assignment,name="upload-assignment"),
    path("submit-assignment/<pk>", submit_assignment,name="submit-assignment"),
    path("edit-grade/<pk>/<ass_id>", Grades_handler, name="update-grade"),
    path("post-assignment/", assignment_creator, name="post-assignment"),
    path("assignments/",assignments_uploader , name="assignment"),
    path("<pk>", student_data , name="student-data"),
    path("logout/",logout_user, name="logout-user"),
    path("update_data/",update_student, name="update-user"),
    path("edit-details/<pk>/<data>", update_data , name="update-user"),
    path("login/" , login_user , name = "login-user"),
    path("signup/", signup, name="register-user")
]
