from django.db import models
from django.contrib.auth.models import User
from django import forms


### Models ###
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    voter = models.ManyToManyField(User, null=True, blank=True, related_name='question_votes')


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    voter = models.ManyToManyField(User, null=True, blank=True, related_name='answer_votes')


### Forms ###
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }
