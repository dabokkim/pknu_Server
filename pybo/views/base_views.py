from django.core.paginator import Paginator # 페이지만들기 클래스(게시판 페이징 기능 추가)
from django.shortcuts import render, get_object_or_404, redirect  # render : 화면에 그려줌 , # redirect : 해당사이트로 다이렉트로 이동하게 해주는 라이브러리


from ..models import Question, Answer # .하나면 현재디렉터리, .하나 더붙이면 상위 디렉터리
from django.db.models import Q, Count  # Q : 검색 기능을 갖고있는 클래스


def index(request):
    """
    질문 목록 출력
    """
    page = request.GET.get('page', '1') # get방식으로 값을 얻어옴
    kw = request.GET.get('kw', '') # 해당 키워드에 대한 검색어를 넘겨줌 , 디폴트가 빈값
    so = request.GET.get('so', 'recent')

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')  # order_by : 정렬해줌 , -붙이면 내림차순으로 정렬



    if kw:
        question_list = question_list.filter( # 필터링해줌
            Q(subject__icontains=kw) | # 제목 검색, subject__icontains : 제목(개별적)에 대한 중복처리
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이
        ).distinct() # distinct() : 전체 결과에 대한 중복처리

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지네이터 객체생성 , 10개씩 자름
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj, 'page':page, 'kw':kw, 'so':so}  # {key, value}형태(딕셔너리) , 현재 페이지의 객체가 넘어옴
    return render(request, 'pybo/question_list.html', context)  # '' : 템플릿(붕어빵 기계)을 만듬

def detail(request, question_id):
    """
    질문 내용 출력
    """
    question = get_object_or_404(Question, pk = question_id) # 받아온 id값을 넘겨줌, #pk : primary key
    context = {'question': question}  # {key, value}형태(딕셔너리)
    return render(request, 'pybo/question_detail.html', context)  # '' : 템플릿(붕어빵 기계)을 만듬
