from .models import Question, Answer
from rest_framework import serializers

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        # fields = ['subject', 'content']   # 특정 필드만 추가
        # exclude = ['author']              # 특정 필드만 제외

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
