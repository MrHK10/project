from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'  # You can specify the fields you want to include here if you don't want all fields
