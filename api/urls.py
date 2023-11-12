from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path , include

router = DefaultRouter()
router.register(r'StudentApiview', StudeDetailPIView, basename='StudentApiview')


urlpatterns = [
 path("", detail_view , name="StudentApi") ,
 path("mark_attendance/<pk>",AttendanceViewSet.as_view({"patch":"update_attendance"}), name="update-attendance")
]
