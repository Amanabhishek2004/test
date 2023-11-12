from django.shortcuts import render , redirect
from datetime import datetime , timedelta
from .models import *
import requests
# Create your views here.

def home(request):
        response = requests.get("http://127.0.0.1:8000/api/").json()
        return render(request , "HOME.HTML" , {"obj":response})


def student_data(request ,pk):
        student = Student.objects.get(id = pk)
        context = {
                "obj":student.subjects.all(),
                "stu":student
        }
        return render(request , "CRUD.html" , context)



def update_data(request,pk,data):
  student_name = request.GET.get("name")
#   print(student_name)
  print(data)
  print(pk)
  print(student_name)
  user_obj = User.objects.get(username = student_name)
  student = Student.objects.filter(name = user_obj ).first()
  count = Count.objects.filter(name__name = student.name).first()
#   print(student)
  if student:
     if count == None: 
      a = Count.objects.create(
          name = student
   )
#      print(a.name.name)
     count_value = Count.objects.filter(name__name = student.name).first()
#      print(count_value)
     current_time_naive = datetime.now()
     current_time = current_time_naive.replace(tzinfo=count_value.updated.tzinfo)
     if data=="present":
         if count_value.updated - current_time >= timedelta(days=1):
             requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
             count_value.present = "marked"
             count_value.absent = "unmarked"
             count_value.save()

         if count_value.present == "marked":      
             return redirect("student-data" ,pk = student.pk)
         
         elif count_value.absent == "marked":
             requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
             count_value.present = "marked"
             count_value.absent = "unmarked"
             count_value.save()
             
         
         else:
             requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
             count_value.present = "marked"
             count_value.save()
             
                   
     if data == "absent":
          
          if count_value.updated - current_time >= timedelta(days=1):
             requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
             count_value.present = "marked"
             count_value.absent = "unmarked"
             count_value.save()


          if count_value.absent == "marked":      
             return redirect("student-data" ,pk = student.pk)
         
          elif count_value.present == "marked":
             requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
             count_value.absent = "marked"
             count_value.present = "unmarked"
             count_value.save()
             
         
          else:
             requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
             count_value.absent = "marked"
             count_value.save()               

   
  return redirect("student-data" ,pk = student.pk)