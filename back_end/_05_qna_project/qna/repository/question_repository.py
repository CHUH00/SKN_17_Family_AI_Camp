from abc import ABC, abstractmethod
from django.db.models import Q
from qna.entity.models import Question, Answer
from django.db.models import Prefetch


class QuestionRepository(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def save(self, question):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def find_by_subject(self, query):
        pass

    @abstractmethod
    def add_remove_voter(self, answer_id, voter):
        pass


class QuestionRepositoryImpl(QuestionRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_all(self):
        # return Question.objects.all().order_by('-created_at') # N+1 이슈
        return Question.objects.prefetch_related('author', 'answer_set').order_by('-created_at') # answer author 이슈

    def find_by_id(self, id):
        return Question.objects.get(id=id)

    def save(self, question):
        question.save()
        return question

    def delete(self, id):
        return Question.objects.filter(id=id).delete()

    def find_by_subject(self, query):
        # return Question.objects.filter(subject__icontains=query).order_by('-created_at')    # 제목만 검색
        return Question.objects.filter(Q(subject__icontains=query) | Q(content__icontains=query)).order_by('-created_at') # 제목, 내용 검색

    def add_remove_voter(self, question, voter):
        if question.voter.filter(id=voter.id).exists():
            question.voter.remove(voter)
        else:
            question.voter.add(voter)