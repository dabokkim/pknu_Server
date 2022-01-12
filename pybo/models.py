from django.db import models
from django.contrib.auth.models import User

# makemigrations : 모델 생성 또는 변경
# migrate : db 테이블 생성
# q.answer_set.all() : 질문하나에 달린 모든 답변을 가져옴

# Create your models here.
class Question(models.Model) : #질문 클래스
    subject = models.CharField(max_length=200) #제목 입력시 최대 몇자까지 입력
    content = models.TextField() #글자 여러줄 입력,글자수 제한x
    create_date = models.DateTimeField() # 현재날짜
    modify_date = models.DateTimeField(null=True, blank=True) # null=True : db에서 컬럼에 null을 허용함, blank=True : 값이 없어도 상관없음(공백도 허용함)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject #subject리턴

class Answer(models.Model) : #답변 클래스
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #연결된 질문 삭제시 답변도 함께 삭제
    content = models.TextField()
    create = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)