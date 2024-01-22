from django import forms
from api.models import *
from django import forms


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = assignements
        fields = ["data", "submitted_to", "is_draft"]


class GradeForm(forms.ModelForm):
    
    class Meta:
        model = Grade
        fields = ["value"]

