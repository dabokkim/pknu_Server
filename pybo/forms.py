from django import forms
from pybo.models import Question, Answer # Question 객체의 속성을 사용하기위함

class QuestionForm(forms.ModelForm) :  # Modelform으로부터 상속받음
    class Meta :
        model = Question
        fields = ['subject', 'content']

        labels = {
            'subject' : '제목',
            'content': '내용'
        }

class AnswerForm(forms.ModelForm) :  # Modelform으로부터 상속받음
    class Meta :
        model = Answer
        fields = ['content']

        labels = {
            'content' : '답변 내용'
        }