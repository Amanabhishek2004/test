from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path , include

router = DefaultRouter()
router.register(r'StudentApiview', StudeDetailPIView, basename='StudentApiview')


urlpatterns = [
 path("", detail_view , name="StudentApi") ,
 path("mark_attendance/<pk>",AttendanceViewSet.as_view({"patch":"update_attendance"}), name="update-attendance"),


     # The endpoint to create a new student
    # The endpoint to retrieve, update, and delete a student by ID
 path('students/<int:id>/', Individual_Student_Api.as_view(), name='individual_student'),
]
