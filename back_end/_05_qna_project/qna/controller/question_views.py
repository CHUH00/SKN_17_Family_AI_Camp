from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from qna.entity.models import QuestionForm
from qna.service.question_service import QuestionServiceImpl

question_service = QuestionServiceImpl.get_instance()


def question_detail(request, question_id):
    question = question_service.find_by_id(question_id)
    return render(request, 'qna/question_detail.html', {"question": question})


@login_required(login_url='uauth:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question = question_service.create(question)
            return redirect('qna:question_detail', question_id=question.id)
        else:
            print('form.errors =', form.errors)
            
    else:
        form = QuestionForm()
        
    return render(request, 'qna/question_form.html', {'form': form})


@login_required(login_url='uauth:login')
def question_modify(request, question_id):
    question = question_service.find_by_id(question_id)

    if request.user != question.author:
        messages.error('request', '수정 권한이 없습니다.')
        return redirect('qna:question_detail', question_id=question_id)

    if request.method == 'POST':
        form= QuestionForm(request.POST, instance=question)
        
        if form.is_valid():
            question = form.save(commit=False)
            question = question_service.modify(question)
            return redirect('qna:question_detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'qna/question_form.html', {'form': form})


@login_required(login_url='uauth:login')
def question_delete(request, question_id):
    question = question_service.find_by_id(question_id)

    if request.user != question.author:
        messages.error('request', '삭제 권한이 없습니다.')
        return redirect('qna:question_detail', question_id=question_id)

    del_question = question_service.delete(question_id)
    messages.success(request, '정상적으로 질문을 삭제했습니다.')
    
    return redirect('qna:index')


### ajax ###
def question_search(request):
    query = request.GET.get('query')
    questions = question_service.find_by_subject(query)
    results = [{'id': question.id, 'text': question.subject} for question in questions]
    return JsonResponse({"results": results})


@login_required(login_url='uauth:login')
def question_vote(request, question_id):
    try:
        question = question_service.add_remove_voter(question_id, request.user)
        votes_count = question.voter.count() if hasattr(question, 'voter') else 0

        return JsonResponse({
            'result': 'success',
            'votes_count': votes_count
        })
    except Exception as e:
        return JsonResponse({
            'result': 'error',
            'message': str(e)
        }, status=400)
