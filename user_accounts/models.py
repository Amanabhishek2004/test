from django.db import models
from django.db.models.signals import post_save
from api.models import *



class Count(models.Model):
     value = models.IntegerField(default = 0)
     name = models.ForeignKey(Student , on_delete=models.CASCADE , null=True)
     subject_name = models.CharField(max_length = 25 , null = True)
     present = models.CharField(default="unmarked" , max_length=20)
     absent = models.CharField(default="unmarked" , max_length=20)
     created = models.DateTimeField( auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)     
     def __str__(self) -> str:
          return self.name.name.username
     

@receiver(post_save, sender=Student)
def create_child_model(sender, instance, created, **kwargs):
    if not created:
        subjects = instance.subjects.all()
        for i in subjects:
            Count.objects.create(name=instance, subject_name=i.name)