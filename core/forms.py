from django import forms
from .models import *

class CreateSurveyForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['survey_title', 'answer_1', 'answer_2', 'answer_3', 'answer_4']