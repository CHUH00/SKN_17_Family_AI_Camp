from django.core.paginator import Paginator
from django.shortcuts import render
from qna.service.question_service import QuestionServiceImpl

question_service = QuestionServiceImpl.get_instance()

def index(request):
    questions = question_service.find_all()
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, 10)
    page_obj = paginator.get_page(page)

    return render(request, 'qna/question_list.html', {'page_obj': page_obj})
