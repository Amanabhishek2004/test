from rest_framework import serializers
from .models import *


from rest_framework import serializers
from .models import Student, Subject, Attendance

class StudentSerializer(serializers.ModelSerializer):
    Attendance_in_each_subject = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "name", "attendance_status", "Attendance_in_each_subject"]

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



