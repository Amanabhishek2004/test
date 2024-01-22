from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path , include


router = DefaultRouter()
router.register(r'StudentApiview', StudeDetailPIView, basename='StudentApiview')


urlpatterns = [
 path("", detail_view , name="StudentApi") ,
 path("mark_attendance/<pk>",AttendanceViewSet.as_view({"patch":"update_attendance"}), name="update-attendance"),
 path("data/<pk>",AssignmentsHandler.as_view(), name="assignment"),
 path('your-model/', assignement_view.as_view(), name='your-model-list'),
 path('students/<int:id>/', Individual_Student_Api.as_view(), name='individual_student'),
 path('grades/<pk>/', Grading.as_view(), name='grade')

]
