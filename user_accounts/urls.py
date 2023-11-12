from django.urls import path
from .views import *

urlpatterns = [
    path("", home , name="home"),
    path("<pk>", student_data , name="student-data"),
    path("edit-details/<pk>/<data>", update_data , name="update-user")
]
