from rest_framework import serializers
from .models import *
from rest_framework import serializers
from .models import Student, Subject, Attendance


from django import forms







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
        fields = ["id", "name","individual_data", "attendance_status", "Attendance_in_each_subject" ,]

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
            subs = Subject.objects.all()
            for i in subs:
                student_instance.subjects.add(i)
                
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
     
    






