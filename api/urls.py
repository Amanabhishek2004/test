from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path , include

router = DefaultRouter()
router.register(r'StudentApiview', StudeDetailPIView, basename='StudentApiview')


urlpatterns = [
 path("", detail_view , name="StudentApi") 
]
