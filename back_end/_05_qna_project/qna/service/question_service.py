from abc import ABC, abstractmethod
from qna.repository.question_repository import QuestionRepositoryImpl


class QuestionService(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def create(self, question):
        pass

    @abstractmethod
    def modify(self, question):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def find_by_subject(self, query):
        pass

    @abstractmethod
    def add_remove_voter(self, question_id, voter):
        pass


class QuestionServiceImpl(QuestionService):
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__question_repository = QuestionRepositoryImpl.get_instance()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_all(self):
        return self.__question_repository.find_all()

    def find_by_id(self, id):
        return self.__question_repository.find_by_id(id)

    def create(self, question):
        return self.__question_repository.save(question)

    def modify(self, question):
        return self.__question_repository.save(question)

    def delete(self, id):
        return self.__question_repository.delete(id)

    def find_by_subject(self, query):
        return self.__question_repository.find_by_subject(query)

    def add_remove_voter(self, question_id, voter):
        question = self.__question_repository.find_by_id(question_id)
        if voter == question.author:
            raise RuntimeError('본인이 작성한 글은 추천할 수 없습니다')
        else:
            # voter가 이미 추천한 글이면 추천 취소, 아니면 추천
            self.__question_repository.add_remove_voter(question, voter)
        return question