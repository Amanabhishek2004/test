from django.shortcuts import render
from rest_framework import viewsets ,generics
from django.views.generic import CreateView
from rest_framework import mixins
from .serializers import *
# Create your views here.

class StudeDetailPIView(generics.ListCreateAPIView):
               serializer_class = StudentSerializer
               queryset = Student.objects.all()

               def get_queryset(self):
                 request = self.request                
                 data =  super().get_queryset()
                 if request.user.is_staff:
                    return data
                 else:
                    return data.filter(name = request.user.username)
                 
detail_view = StudeDetailPIView.as_view()
               

        