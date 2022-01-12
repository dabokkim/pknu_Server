from django.shortcuts import render, get_object_or_404, redirect  # render : 화면에 그려줌 , # redirect : 해당사이트로 다이렉트로 이동하게 해주는 라이브러리
# from django.http import HttpResponse
from .models import Question, Answer
from django.utils import timezone   #답변달 때 시간 표시를 위한 라이브러리
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator # 페이지만들기 클래스(게시판 페이징 기능 추가)
from django.contrib.auth.decorators import login_required # 로그인 페이지로 이동하게함
from django.contrib import messages # messages함수 추가


# Create your views here.
def index(request):
    """
    질문 목록 출력
    """
    page = request.GET.get('page', '1') # get방식으로 값을 얻어옴

    question_list = Question.objects.order_by('-create_date')  # order_by : 정렬해줌 , -붙이면 내림차순으로 정렬

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지네이터 객체생성 , 10개씩 자름
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj}  # {key, value}형태(딕셔너리) , 현재 페이지의 객체가 넘어옴
    return render(request, 'pybo/question_list.html', context)  # '' : 템플릿(붕어빵 기계)을 만듬

def detail(request, question_id):
    """
    질문 내용 출력
    """
    question = get_object_or_404(Question, pk = question_id) # 받아온 id값을 넘겨줌, #pk : primary key
    context = {'question': question}  # {key, value}형태(딕셔너리)
    return render(request, 'pybo/question_detail.html', context)  # '' : 템플릿(붕어빵 기계)을 만듬

@login_required(login_url='common:login') # 로그인이 반드시 필요하다는 것을 표시, common의 login으로 페이지 이동함
def answer_create(request, question_id):
    """
    답변 등록
    """
    question = get_object_or_404(Question, pk = question_id) # 받아온 id값을 넘겨줌, #pk : primary key

    if request.method == "POST" : #POST방식일때 처리방식
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id) # 답변등록 후 현재화면 유지
    else :
        form = AnswerForm() #객체 생성

    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context) # 답변등록 클릭 시 question_detail.html 파일로 이동

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


@login_required(login_url='common:login') # 로그인이 반드시 필요하다는 것을 표시, common의 login으로 페이지 이동함
def answer_modify(request, answer_id):
    """
    답변 수정
    """
    answer = get_object_or_404(Answer, pk = answer_id) # 받아온 id값을 넘겨줌, #pk : primary key
    if request.user != answer.author : # 사용자 아이디와 수정하려는 사용자가 일치 하지않을 때
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = answer.question.id) # answer에 속한 question id를 넘겨줌

    if request.method == "POST" : #POST방식일때 처리방식
        form = AnswerForm(request.POST, instance=answer) # instance : 고유한 값을 갖게함
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id) # 답변등록 후 현재화면 유지
    else :
        form = AnswerForm(instance=answer) #객체 생성

    context = {'answer' : answer, 'form' : form}
    return render(request, 'pybo/answer_form.html', context) # 답변등록 클릭 시 question_detail.html 파일로 이동

@login_required(login_url='common:login') # 로그인이 반드시 필요하다는 것을 표시, common의 login으로 페이지 이동함
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    # 예외처리
    answer = get_object_or_404(Answer, pk = answer_id) # 받아온 id값을 넘겨줌, #pk : primary key
    if request.user != answer.author : # 사용자 아이디와 수정하려는 사용자가 일치 하지않을 때
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id) # 답변삭제 후 현재화면 유지




# return HttpResponse("Hello World")

