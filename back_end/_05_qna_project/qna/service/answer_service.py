from abc import ABC, abstractmethod
from qna.entity.models import Answer
from qna.repository.answer_repository import AnswerRepositoryImpl
from qna.repository.question_repository import QuestionRepositoryImpl


class AnswerService(ABC):

    @abstractmethod
    def create(self, question_id, content, author):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def delete(self, answer):
        pass

    @abstractmethod
    def modify(self, answer):
        pass

    @abstractmethod
    def add_remove_voter(self, answer_id, voter):
        pass


class AnswerServiceImpl(AnswerService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__answer_repository = AnswerRepositoryImpl.get_instance()
        self.__question_repository = QuestionRepositoryImpl.get_instance()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def create(self, question_id, content, author):
        # question 유효 검증
        question = self.__question_repository.find_by_id(question_id)
        # 사용자 입력 값을 answer 모델 객체로 변환
        answer = Answer(question=question, content=content, author=author)
        return self.__answer_repository.save(answer)

    def find_by_id(self, id):
        return self.__answer_repository.find_by_id(id)

    def delete(self, answer):
        return self.__answer_repository.delete(answer)

    def modify(self, answer):
        return self.__answer_repository.save(answer)

    def add_remove_voter(self, answer_id, voter):
        answer = self.__answer_repository.find_by_id(answer_id)
        if voter == answer.author:
            raise RuntimeError('본인이 작성한 답글은 추천할 수 없습니다')
        else:
            # voter가 이미 추천한 글이면 추천 취소, 아니면 추천
            self.__answer_repository.add_remove_voter(answer, voter)
        return answer