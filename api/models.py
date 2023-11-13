from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
      name = models.CharField(max_length=20)
      No_of_classes = models.IntegerField()
      no_of_required_classes = models.IntegerField()
      
      def  __str__(self) -> str:
            return self.name

@receiver(pre_save, sender=Subject)
def _post_save_receiver(sender,instance , **kwargs):
      instance.no_of_required_classes = instance.No_of_classes*0.75
          
      
class Student(models.Model):
      name = models.ForeignKey(User , on_delete=models.CASCADE  ,null = True , blank = True)
      # name = models.CharField(max_length=25)
      attendance_status = models.CharField(max_length=7)
      subjects = models.ManyToManyField(Subject)

      def __str__(self) -> str:
            return self.name.username



class Attendance(models.Model):
      subject = models.ForeignKey(Subject , on_delete= models.CASCADE)
      student = models.ForeignKey(Student , on_delete= models.CASCADE , null = True)
      no_of_classes_attended = models.IntegerField()

      def __str__(self) -> str:
            return f"{self.student}----{self.subject}------{self.no_of_classes_attended}"

