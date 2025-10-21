from django.urls import path, include
from rest_framework.routers import DefaultRouter
from qna.views import QuestionViewSet, AnswerViewSet
from rest_framework_nested.routers import NestedSimpleRouter

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

questions_router = NestedSimpleRouter(router, r'questions', lookup='question')
questions_router.register(r'answers', AnswerViewSet, basename='question-answers')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(questions_router.urls)),
]
