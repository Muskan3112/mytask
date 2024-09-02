from django import forms
from .models import MyTaskList

class TaskFilterForm(forms.Form):
    titles = forms.ModelMultipleChoiceField(
        queryset=MyTaskList.objects.values_list('title', flat=True).distinct(),
        widget=forms.SelectMultiple,
        required=False
    )
    due_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))