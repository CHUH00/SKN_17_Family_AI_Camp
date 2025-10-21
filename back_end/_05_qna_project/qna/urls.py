from django.urls import path
from qna.controller import views, question_views, answer_views

app_name = 'qna'

urlpatterns = [
    # 기본 view
    path('', views.index, name='index'),

    # question관련 view
    path('question/<int:question_id>/', question_views.question_detail, name='question_detail'),
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),

    # question관련 view - ajax
    path('question/search/', question_views.question_search, name='question_search'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    # answer관련 view
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),

    # answer관련 view - ajax
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),
]