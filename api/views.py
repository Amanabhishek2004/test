from django.shortcuts import render
from rest_framework import viewsets ,generics
from django.views.generic import CreateView
from rest_framework import mixins 
from rest_framework.views import APIView
from .serializers import *
from user_accounts.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

class StudeDetailPIView(generics.ListCreateAPIView):
               queryset = Student.objects.all()
            
               lookup_field = "id"
               def get_serializer_class(self):
                 if self.request.method in ["POST", "PUT", "PATCH"]:
                     return StudentSerializer
                 else:
                    return StudentReadSerializer
                     
            #    def get_queryset(self):
            #     #  request = self.request                
            #     #  data =  Student.objects.all()
            #     #  if request.user.is_staff:
            #     #     return data
            #     #  else:
            #     #     return data.filter(name = request.user)
                 

detail_view = StudeDetailPIView.as_view()
               
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"

    @action(detail=True, methods=['patch'])
    def update_attendance(self, request, pk=""):
        # Assuming 'pk' is the subject name
        name = request.GET.get("name")
        
        try:
            user_instance = User.objects.get(username=name)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        attendance_instance = Attendance.objects.filter(student__name=user_instance, subject__name=pk).first()

        if attendance_instance:
            data = request.GET.get("value")

            if data == "absent":
                attendance_instance.no_of_classes_attended-=1
                attendance_instance.save()
                return Response({"done": 1}, status=200)
            elif data == "present":
                attendance_instance.no_of_classes_attended += 1
                attendance_instance.save()
                return Response({"response": attendance_instance.no_of_classes_attended}, status=200)

        return Response({"response": "Attendance instance not found"}, status=404)

AttendanceViewSet.as_view({"patch":"update_attendance"})

class Individual_Student_Api(generics.CreateAPIView , generics.DestroyAPIView , generics.RetrieveUpdateAPIView):
      
      queryset = Student.objects.all()
      lookup_field = "id"
      def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return StudentSerializer
        else:
         return StudentReadSerializer
        






