from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin) : #검색기능
    search_fields = ['subject'] #제목으로 검색

# Register your models here.
admin.site.register(Question, QuestionAdmin) # Question 모델 등록

# python manage.py createsuperuser : admin계정만들기