from django.shortcuts import render , redirect
from datetime import datetime , timedelta
from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login , logout
import requests
from django.utils import timezone
# Create your views here.
from django import forms

def home(request):
        print(request.user.id)
        
        
        if  request.user.is_staff:
         
         response = requests.get(f"http://127.0.0.1:8000/api/").json()  
        
        else:
         stu = Student.objects.get(name = request.user)
         response = requests.get(f"http://127.0.0.1:8000/api/students/{stu.pk}").json()

        return render(request , "HOME.HTML" , {"obj":response})


def student_data(request,pk):
        student = Student.objects.get(id = pk)
        data = Attendance.objects.filter(student = student)
        context = {
                # "obj":student.subjects.all(),
                "stu":student,
                "data":data
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
         if current_time - count_value.updated >= timedelta(seconds=1) and (count_value.present == "marked" or count_value.present == "unmarked" ):
             print(count_value.updated - current_time)
             requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
             count_value.present = "marked"
             count_value.absent = "unmarked"
             count_value.updated.replace(tzinfo=timezone.utc)
             count_value.save()

         if count_value.present == "marked":
             print(count_value.updated - current_time)      
             return redirect("student-data" ,pk = student.pk)
         
         elif count_value.absent == "marked":
             response = requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
             print(response.json())
             count_value.present = "marked"
             count_value.absent = "unmarked"
             count_value.save()
             
         
         else:
             requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
             count_value.present = "marked"
             count_value.save()
             
                   
     if data == "absent":
          
          if current_time-count_value.updated >= timedelta(days=1):
            #  requests.patch(f"http://127.0.0.1:8000/api/mark_attendance/{pk}?value={data}&name={student_name}")
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


def login_user(request):
   

    page = 'login'

    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('you are not a registered user')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, 'login.html' , {"page":page})


def logout_user(request):
    logout(request)

    return redirect("login-user")



def signup(request):
    if request.method == 'POST':
        if not User.objects.filter(username=request.POST["username"]).exists() and request.POST['password1'] == request.POST['password']:
            # Create data for the StudentSerializer
            student_data = {
                "name": {
                    "username": request.POST['username'],
                    "email": request.POST['email'],
                    "password": request.POST['password1']
                },
                "attendance_status": "GOOD"  # Replace with actual value
            }

            # Make a POST request to the API
            api_url = 'http://127.0.0.1:8000/api/'
            response = requests.post(api_url, json=student_data)
            print(response.json())

            
          

    return render(request, 'REGISTER.html')


class UpdateStudentForm(forms.Form):
 
    email = forms.EmailField()
    



from django.contrib.auth.decorators import login_required



@login_required(login_url="login-user")
def update_student(request):
    form = UpdateStudentForm(request.POST or None, initial={
      
        'email': request.user.email
        
       # Replace with actual value
    })
    
    student = Student.objects.get(name = request.user)

    if request.method == 'POST':
        if form.is_valid():
            # Create data for the StudentSerializer
            student_data = {
                'name': {
                    
                    'email': form.cleaned_data['email']
                    
                }
         
            }

            # Make a PUT or PATCH request to the API
            api_url = f'http://127.0.0.1:8000/api/students/{student.pk}/'
            response = requests.patch(api_url, json=student_data)
            print(response)
            
            

    return render(request, 'update.html', {'form': form})


