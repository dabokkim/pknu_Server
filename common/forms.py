from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm) : # UserCreationForm 을 상속받음 , 사용자정의 클래스
    email = forms.EmailField(label="이메일")
    
    class Meta : #Meta클래스는 제공되는 클래스 , 이너클래스생성
        model = User
        fields = ("username", "password1", "password2", "email")