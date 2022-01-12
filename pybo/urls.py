from django.urls import path
from .views import base_views, question_views, answer_views # views폴더 내 각각의 파일을 import함

# namespace기법 : 중복을 피하기 위하여 사용
app_name = 'pybo'

urlpatterns = [
    path('', base_views.index, name = 'index'), # name : 별칭
    path('<int:question_id>/', base_views.detail, name = 'detail'),
    path('answer/create/<int:question_id>/', answer_views.answer_create, name = 'answer_create'),
    path('question/create/', question_views.question_create, name = 'question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name = 'question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name = 'question_delete'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name = 'answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name = 'answer_delete'),
]
