from rest_framework import serializers
from .models import *
from rest_framework import serializers
from .models import Student, Subject, Attendance
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response



class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ["id", "value"]

    def update(self, instance, validated_data):

      request = self.context.get("request")
      username = request.GET.get("name")
      assignement_id = request.GET.get("id")
      staff = staff_data.objects.filter(name = User.objects.get(username = username)  )
      assignements_obj = assignements.objects.get(id = assignement_id)
      if staff!= None and (assignements_obj.submitted_to == staff.first() or staff.first().designation == "Principle") and assignements_obj.is_draft == "False":
        value = validated_data.get("value", instance.value)
        instance.value = value
        instance.save()

      return instance

class AssignmentSerializer(serializers.ModelSerializer):
    Assignment_status = serializers.SerializerMethodField(read_only = True)
    file_name = serializers.SerializerMethodField(read_only = True)
    file = serializers.FileField(write_only=True ,required = False ,  allow_null = True)
    grade = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = assignements
        fields = ["id", "student" , "is_draft" , "subject" , "Assignment_status" , "file" , "file_name" , "grade" , "submitted_to"]
    
    def get_file_name(self , obj):
      if obj:  
        return obj.data.name
    
    def get_grade(self , obj):
        if Grade.objects.filter(assignement = obj):
           
           serialized_data = GradeSerializer(Grade.objects.filter(assignement = obj).first())

           return serialized_data.data
        
        else:
            return "not given still"



    def get_Assignment_status(self,obj):

        if obj.is_draft=='False':
            return "SUBITTED"
        
        else:
            return "SUBMITTED AS DRAFT"
    def create(self, validated_data):
        print(validated_data)
        file = validated_data.get("data")
        if file:
            pass
        return super().create(validated_data)     
        
    def update(self, instance, validated_data):
     print(validated_data)
     file = validated_data.pop("file", None)
     if file and instance.is_draft == "True":
        instance.data = file
     elif file and instance.is_draft == "False":
        return serializers.ValidationError({
            "Message": "You can't upload the file now."
        })
      
     if validated_data.get("is_draft"):
       instance.is_draft = validated_data.get("is_draft")

     if validated_data.get("is_draft") == "False":
        if Grade.objects.filter(assignement = instance): 
             pass
        else:
          Grade.objects.create(assignement = instance)
       
     instance.subject = validated_data.get("subject", instance.subject)
    
    # Save only if is_draft is True or the file was uploaded
     if instance.is_draft or file:
        instance.save()

     instance.Assignment_status = self.get_Assignment_status(instance)
     return instance




class userserilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username" , "email" , "password"]




class StudentSerializer(serializers.ModelSerializer):
    Attendance_in_each_subject = serializers.SerializerMethodField(read_only=True)
    individual_data = serializers.SerializerMethodField(read_only =True)
    name = userserilizer(write_only = True)
    class Meta:
        model = Student
        fields = ["id", "name","individual_data", "attendance_status", "Attendance_in_each_subject",]

    def get_Attendance_in_each_subject(self, obj):
        qs = obj.subjects.all()
        data = []
        for subject in qs:
            record = {
                "subject_name": subject.name,
                "classes_required_to_attend": subject.no_of_required_classes,
            }
            attendance_record = Attendance.objects.filter(student=obj, subject=subject).first()
            if attendance_record:
                record["no_of_classes_attended"] = attendance_record.no_of_classes_attended
            else:
                record["no_of_classes_attended"] = 0

            data.append(record)

        return data
    
    def get_individual_data(self , obj):
        pk = obj.pk
        return f"http://127.0.0.1:8000/api/students/{pk}/"  
    

    def create(self, validated_data):

      # Extract the data for the nested serializer (name)
        name_data = validated_data.pop('name', None)

        # Create the Student instance
        student_instance = Student.objects.create(**validated_data)      
    
        if name_data:
            # If "name" field is a nested serializer, create User separately
            user_serializer = userserilizer(data=name_data)
            user_serializer.is_valid(raise_exception=True)
            user_instance = user_serializer.save()
            # Assign the created User instance to the Student
            student_instance.name = user_instance
            student_instance.save()

        return student_instance
    def update(self, instance, validated_data):
        # Update the email field if it's present in the validated_data
        name_data = validated_data.pop('name', None)
        if name_data:
            user_instance = instance.name
            user_serializer = userserilizer(instance=user_instance, data={'email': name_data.get('email')}, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        return super().update(instance, validated_data) 
    


class StudentReadSerializer(serializers.ModelSerializer):
    Attendance_in_each_subject = serializers.SerializerMethodField(read_only=True)
    individual_data = serializers.SerializerMethodField(read_only =True)
    name = userserilizer()
    class Meta:
        model = Student
        fields = ["id","name","individual_data","attendance_status","Attendance_in_each_subject"]

    def get_Attendance_in_each_subject(self, obj):
        qs = obj.subjects.all()
        data = []
        for subject in qs:
            record = {
                "subject_name": subject.name,
                "classes_required_to_attend": subject.no_of_required_classes,
            }
            attendance_record = Attendance.objects.filter(student=obj, subject=subject).first()
            if attendance_record:
                record["no_of_classes_attended"] = attendance_record.no_of_classes_attended
            else:
                record["no_of_classes_attended"] = 0

            data.append(record)

        return data
    
    

    def get_individual_data(self , obj):
        pk = obj.pk
        return f"http://127.0.0.1:8000/api/students/{pk}/"  
     
    






