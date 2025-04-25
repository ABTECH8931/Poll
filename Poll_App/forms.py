from django import forms
from .models import Question, Choice

# Create your forms here.
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']