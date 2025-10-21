from abc import ABC, abstractmethod
from qna.entity.models import Answer


class AnswerRepository(ABC):
    @abstractmethod
    def save(self, answer):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def delete(self, answer):
        pass

    @abstractmethod
    def add_remove_voter(self, answer, voter):
        pass


class AnswerRepositoryImpl(AnswerRepository):
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

    def save(self, answer):
        answer.save()
        return answer

    def find_by_id(self, id):
        return Answer.objects.get(id=id)

    def delete(self, answer):
        return answer.delete()

    def add_remove_voter(self, answer, voter):
        if answer.voter.filter(id=voter.id).exists():
            answer.voter.remove(voter)
        else:
            answer.voter.add(voter)