from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, resolve_url
from qna.service.answer_service import AnswerServiceImpl

answer_service = AnswerServiceImpl.get_instance()


@login_required(login_url='uauth:login')
def answer_create(request, question_id):
    content = request.POST.get('content')
    author = request.user
    answer = answer_service.create(question_id, content, author)
    return redirect(f'{resolve_url('qna:question_detail', question_id=question_id)}#answer_{answer.id}')


@login_required(login_url='uauth:login')
def answer_delete(request, answer_id):
    question_id = request.GET['question_id']
    answer = answer_service.find_by_id(answer_id)

    if request.user != answer.author:
        messages.error('request', '삭제 권한이 없습니다.')
        return redirect('qna:question_detail', question_id=question_id)

    del_answer = answer_service.delete(answer)
    messages.success(request, '정상적으로 답변을 삭제했습니다.')
    return redirect('qna:question_detail', question_id=question_id)


@login_required(login_url='uauth:login')
def answer_modify(request, answer_id):
    question_id = request.GET['question_id']
    answer = answer_service.find_by_id(answer_id)

    if request.user != answer.author:
        messages.error('request', '수정 권한이 없습니다.')
        return redirect('qna:question_detail', question_id=question_id)

    if request.method == 'POST':
        new_content = request.POST['content']
        answer.content = new_content
        answer = answer_service.modify(answer)

    return redirect('qna:question_detail', question_id=question_id)


### ajax ###
@login_required(login_url='uauth:login')
def answer_vote(request, answer_id):
    try:
        answer = answer_service.add_remove_voter(answer_id, request.user)
        votes_count = answer.voter.count() if hasattr(answer, 'voter') else 0
        return JsonResponse({
            'result': 'success',
            'votes_count': votes_count
        })
    except Exception as e:
        return JsonResponse({
            'result': 'error',
            'message': str(e)
        }, status=400)