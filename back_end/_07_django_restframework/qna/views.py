from django.shortcuts import render
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['subject', 'content']
    ordering_fields = ['created_at']

class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
