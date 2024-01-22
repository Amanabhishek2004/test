from django.shortcuts import render
from rest_framework import viewsets ,generics
from .serializers import *
from user_accounts.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
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
                     
                 

detail_view = StudeDetailPIView.as_view()
               

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
        



class Grading(generics.RetrieveUpdateAPIView):
    
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    






class AssignmentsHandler(generics.RetrieveUpdateDestroyAPIView):

    queryset = assignements.objects.all()
    serializer_class = AssignmentSerializer



    """
use the last date to submit assignment
    """


class assignement_view(generics.ListAPIView , generics.CreateAPIView):

    queryset = assignements.objects.all()
    serializer_class = AssignmentSerializer
    
    
    def get_queryset(self):

        user = User.objects.filter(username = self.request.GET.get("username")).first()

        if staff_data.objects.filter(name = user).first() == None:
         subject_name = self.request.query_params.get('Subject', None)
         student_name = self.request.query_params.get('student_name', None)
         queryset = self.queryset      
         queryset = queryset.filter(subject = Subject.objects.filter(name = subject_name).first() ,student__name=User.objects.filter(username = student_name).first())
        
        elif  staff_data.objects.filter(name = user).first().designation == "Teacher":
          subject_name = self.request.query_params.get('Subject', None)
          student_name = self.request.query_params.get('student_name', None)
          queryset = self.queryset
          queryset = queryset.filter(submitted_to = staff_data.objects.filter(name = user).first() , subject = Subject.objects.filter(name = subject_name).first() ,student__name=User.objects.filter(username = student_name).first() , is_draft = "False")
        
        elif staff_data.objects.filter(name = user).first().designation == "Principle":
           subject_name = self.request.query_params.get('Subject', None)
           student_name = self.request.query_params.get('student_name', None)
           queryset = self.queryset
           queryset = queryset.filter(subject = Subject.objects.filter(name = subject_name).first() ,student__name=User.objects.filter(username = student_name).first()) 
        return queryset


