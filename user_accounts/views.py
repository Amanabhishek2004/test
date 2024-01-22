from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect
from datetime import datetime , timedelta
from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login , logout
import requests
from django.utils import timezone
from django import forms
from .forms import *


def home(request):
    if request.user.is_authenticated:    
        print(request.user.id)
        if staff_data.objects.filter(name = request.user):         
            response = requests.get(f"http://127.0.0.1:8000/api/").json()  
        
        else:
         stu = Student.objects.filter(name = request.user).first()
         if stu:
            response = [requests.get(f"http://127.0.0.1:8000/api/students/{stu.pk}").json()]
         
        return render(request , "HOME.HTML" , {"obj":response})
    else:
        return redirect("login-user")

def student_data(request,pk):
        student = Student.objects.filter(id = pk).first()
        data = Attendance.objects.filter(student = student)
        staff = staff_data.objects.filter(name = request.user)  
        context = {
                "obj":staff,
                "stu":student,
                "data":data
        }
        return render(request , "CRUD.html" , context)



def update_data(request,pk,data):
  
  student_name = request.GET.get("name")
  print(data)
  print(pk)
  print(student_name)
  
  user_obj = User.objects.get(username = student_name)
  student = Student.objects.filter(name = user_obj ).first()
  subject = Subject.objects.get(name = pk)

  if student:

     count_value = Count.objects.filter(name__name = student.name , subject_name = subject).first()
     current_time_naive = datetime.now()
     current_time = current_time_naive.replace(tzinfo=count_value.updated.tzinfo)
     if data=="present":
         if current_time - count_value.updated >= timedelta(days=1) and (count_value.present == "marked" or count_value.present == "unmarked" ):
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



def assignments_uploader(request):
       
       student = request.GET.get("stu")
       subject = request.GET.get("sub")
       response = requests.get(f"http://127.0.0.1:8000/api/your-model/?Subject={subject}&student_name={student}&username={request.user.username}")
       if (response) :
           response = response.json()

       context = {
           "response":response
       }

       return render(request , "ASSIGNMENTS.html" , context)

def assignment_creator(request):
       student_name = request.GET.get("stu")
       subject_name = request.GET.get("sub") 
       api_endpoint = f"http://127.0.0.1:8000/api/your-model/?Subject={subject_name}&student_name={student_name}&username={request.user.username}"
       form_data = AssignmentForm()
       if request.method == "POST":
           form_data = AssignmentForm(request.POST , request.FILES)
           if form_data.is_valid():
               data = {  
                "student": Student.objects.get(name__username = student_name).id,
                "is_draft": form_data.cleaned_data["is_draft"],
                "subject": Subject.objects.get(name = subject_name).id,
                "submitted_to":form_data.cleaned_data["submitted_to"].id,
            }
           
           response = requests.post(api_endpoint, data=data)
           target = assignements.objects.filter(student__id = data["student"] , subject__id = data["subject"] , submitted_to__id = data["submitted_to"]  , is_draft = data["is_draft"]).order_by("-created_at").first()
           print(target.pk)
           if form_data.cleaned_data["data"]:
              data = {}
              data["file"] = form_data.cleaned_data["data"]
              print(data)
              api_endpoint = f'http://127.0.0.1:8000/api/data/{target.pk}' 
              
              print(requests.patch(api_endpoint , files = data))

       return render(request , "post_assignment.html" , context = {
           "form":form_data
       })

def edit_assignment(request , pk):
    
    if request.method == 'POST' :
            
        uploaded_file = request.FILES.get('fileUpload')
        print(uploaded_file)
        api_endpoint = f'http://127.0.0.1:8000/api/data/{pk}' 
        files = {}
        files['file'] = uploaded_file
        response = requests.patch(api_endpoint, files=files)
        print(response)
    return render(request,"upload_assignments.html")    


def Grades_handler(request, pk , ass_id):
    print(ass_id) 
    api_endpoint = f"http://127.0.0.1:8000/api/grades/{pk}/?id={ass_id}&name={request.user.username}"
    print(api_endpoint)
    grade_instance = Grade.objects.get(id=pk)
    form_data = GradeForm(instance=grade_instance)

    if request.method == 'POST':
        form_data = GradeForm(request.POST)

        if form_data.is_valid():
            data = {
             
                    "value": form_data.cleaned_data["value"]

            }
            response = requests.patch(api_endpoint, json=data)
    return render(request, "Grading.html", context={"form": form_data})


def submit_assignment(request , pk):


       data =  {
           "is_draft":"False"
       }
       requests.patch(f'http://127.0.0.1:8000/api/data/{pk}' , json=data)

       return redirect("home")
    