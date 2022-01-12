from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

def signup(request) :
    """
    계정 생성
    """
    if request.method == "POST" : #POST방식일때 처리방식
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # cleaned_data.get : 입력값을 개별적으로 얻고싶을때 사용
            raw_password = form.cleaned_data.get('password1')
            user =authenticate(username = username, password = raw_password)
            login(request, user) #로그인시 user값 넘겨줌
            return redirect('index')
    else :
        form = UserForm() #객체 생성 (GET방식일 경우)
    return render(request, 'common/signup.html', {'form' : form}) # signup페이지를 렌더링하면서 폼객체를 통째로 넘겨줌


# return HttpResponse("Hello World")

