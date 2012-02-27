from django import forms
from models import Task

class TaskCheckForm(forms.Form):
    task = forms.ModelChoiceField(queryset=Task.objects.all(), required=True)
    task_time = forms.DateTimeField(help_text='Excecution time.', required=True)
    status = forms.CharField(max_length=100, help_text='Status text.  Max length 100 chars.', required=True)
    comment = forms.CharField(help_text='Comment text.', widget=forms.Textarea, required=False)
