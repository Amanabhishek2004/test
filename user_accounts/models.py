from django.db import models
from api.models import *
# Create your models here.
class Count(models.Model):
     value = models.IntegerField(default = 0)
     name = models.ForeignKey(Student , on_delete=models.CASCADE , null=True)
     present = models.CharField(default="unmarked" , max_length=20)
     absent = models.CharField(default="unmarked" , max_length=20)
     created = models.DateTimeField( auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)     
     def __str__(self) -> str:
          return self.name.name.username