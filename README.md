TO RUN THE PROJECT INSTALL ALL THE PACKAGES FROM REQUIREMENTS.TXT
THEN OPEN THE FOLDER WITH VSCODE AND TYPE cd .\Zorway_Assignment
then write python manage.py runserver then go to the link

for viewing the api data of all students  ------ http://127.0.0.1:8000/api/
individual data can also be seen using primary key or just clicking on the student name
for viewing the database go to ------- http://127.0.0.1:8000/admin/



----- login through this to view the staff privileges as a PRINCIPLE

username - VAIDIK
password - AMAN@2004

----- login through this to view the staff privileges as a teacher

username - HARSH
password - AMAN@2004

username - SHUBHAM
password - AMAN@2004

----- login through this to view the student privileges

username = AMAN
password = admin

username = NAMAN
password = AMAN@2004

------ LOGIN THE DATA ABSE THROUGH THIS
username = AMAN
password = admin
I have taken care of staff and student login if staff is there he/she can view all the student data as well as mark present or absent . 

If student logs in  then he can just view his individual data 

I have created present and absent button in such a way that they can be pressed only once in a day to avoid proxy 

I have added here the student assignmnet management and draft facility i.e student can save the assignment as draft uand edit it as draft unil and unless it finally submitted  
The teachers can view only the assignment submitted to them and grade it 
The principle can view any assignment and edit the grade given by the teacher