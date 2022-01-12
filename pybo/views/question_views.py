from django.contrib import messages  # messages함수 추가
from django.contrib.auth.decorators import login_required  # 로그인 페이지로 이동하게함
from django.shortcuts import render, get_object_or_404, redirect  # render : 화면에 그려줌 , # redirect : 해당사이트로 다이렉트로 이동하게 해주는 라이브러리
from django.utils import timezone  # 답변달 때 시간 표시를 위한 라이브러리

from ..forms import QuestionForm
# from django.http import HttpResponse
from ..models import Question


@login_required(login_url='common:login')
def question_create(request) :
    """
    pybo 질문 등록
    """
    if request.method == "POST" : #POST방식일때 처리방식
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')

    else :
        form = QuestionForm() #객체 생성

    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login') # 로그인이 반드시 필요하다는 것을 표시, common의 login으로 페이지 이동함
def question_modify(request, question_id):
    """
    질문 수정
    """
    question = get_object_or_404(Question, pk = question_id) # 받아온 id값을 넘겨줌, #pk : primary key
    if request.user != question.author : # 사용자 아이디와 수정하려는 사용자가 일치 하지않을 때
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)

    if request.method == "POST" : #POST방식일때 처리방식
        form = QuestionForm(request.POST, instance=question) # instance : 고유한 값을 갖게함
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id) # 답변등록 후 현재화면 유지
    else :
        form = QuestionForm(instance=question) #객체 생성

    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context) # 답변등록 클릭 시 question_detail.html 파일로 이동

@login_required(login_url='common:login') # 로그인이 반드시 필요하다는 것을 표시, common의 login으로 페이지 이동함
def question_delete(request, question_id):
    """
    질문 삭제
    """
    question = get_object_or_404(Question, pk = question_id) # 받아온 id값을 넘겨줌, #pk : primary key
    if request.user != question.author : # 사용자 아이디와 수정하려는 사용자가 일치 하지않을 때
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)

    question.delete()
    return redirect('pybo:index') # 답변삭제 후 인덱스화면으로 이동