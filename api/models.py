from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save , post_save
from django.contrib.auth.models import User



class Subject(models.Model):
      name = models.CharField(max_length=20)
      No_of_classes = models.IntegerField(default = 0 )
      no_of_required_classes = models.IntegerField(default = 0)
      
      def  __str__(self) -> str:
            return self.name


@receiver(pre_save, sender=Subject)
def _post_save_receiver(sender,instance , **kwargs):
      instance.no_of_required_classes = instance.No_of_classes*0.75
          
      
class Student(models.Model):
      name = models.ForeignKey(User , on_delete=models.CASCADE  ,null = True , blank = True)
      attendance_status = models.CharField(max_length=7)
      subjects = models.ManyToManyField(Subject)

      def __str__(self) -> str:
            return self.name.username
      

class staff_data(models.Model):
      designation = models.CharField(max_length = 20 , null = True , blank = True)
      name = models.ForeignKey(User , on_delete = models.CASCADE , null = True , blank = True)

      def __str__(self) -> str:
            return f"{self.name.username} ---------> {self.designation}"
      
class assignements(models.Model):
      
      student = models.ForeignKey(Student,on_delete=models.CASCADE)
      submitted_to = models.ForeignKey(staff_data , on_delete = models.CASCADE ,null = True ,blank = True)
      data = models.FileField(upload_to="./assignemnets", max_length=100 , blank=True , null=True)
      subject = models.ForeignKey(Subject , null = True , on_delete = models.CASCADE)
      is_draft = models.CharField( max_length = 24 , null = True)
      created_at = models.DateTimeField(auto_now_add=True , null = True)

      def __str__(self) -> str:
            return f"{self.student.name.username} ------> {self.subject.name}--------->{self.submitted_to.name.username}"

      
@receiver(pre_save, sender=Subject)
def _post_save_receiver(sender,instance,created , **kwargs):
      if created:
         for i in instance.subjects.all():
            Attendance.objects.create(student = instance , subject = i)



class Attendance(models.Model):
      subject = models.ForeignKey(Subject , on_delete= models.CASCADE)
      student = models.ForeignKey(Student , on_delete= models.CASCADE , null = True)
      no_of_classes_attended = models.IntegerField(default = 0)

      def __str__(self) -> str:
            return f"{self.student}----{self.subject}------{self.no_of_classes_attended}"



class Grade(models.Model):
      value = models.CharField(max_length = 25 , null = True)
      assignement = models.ForeignKey(assignements ,on_delete = models.CASCADE , null = True , blank = True)
      student = models.ForeignKey(Student , on_delete = models.CASCADE , null = True , blank = True)