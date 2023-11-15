from django.shortcuts import render
from . import models
from django.http import Http404
from django.core.paginator import Paginator


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    try:
        if page_number:
            page_number = int(page_number)
    except ValueError:
        raise Http404("Page number must be an integer")
    if not page_number or page_number < 1:
        page_number = 1
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages
    page = paginator.get_page(page_number)
    return page, paginator.num_pages


def check_question_id(question_id):
    question_item = models.Question.objects.filter(id=question_id)
    answers = models.Answer.objects.filter(question_id=question_id)
    if question_item.count() == 0:
        raise Http404("Wrong question index")
    return question_item, answers


def index(request):
    questions = models.Question.objects.get_new_questions()
    page, number_of_pages = paginate(questions, request)

    context = {'questions': page, 'number_of_pages': number_of_pages, 'is_authorized': True}
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    question_item, answers = check_question_id(question_id)
    page, number_of_pages = paginate(answers, request)
    context = {'question': question_item[0], 'answers': page, 'number_of_pages': number_of_pages, 'is_authorized': True}
    return render(request, 'question.html', context=context)


def login(request):
    context = {'is_authorized': False, 'error': 'Sorry, wrong password!'}
    return render(request, 'login.html', context=context)


def signup(request):
    context = {'is_authorized': False, 'error': 'Sorry, this email address already registered'}
    return render(request, 'signup.html', context=context)


def settings(request):
    user = models.Profile.objects.get_user_by_username('user0')
    context = {'user': user[0], 'is_authorized': True}
    return render(request, 'settings.html', context=context)


def ask(request):
    context = {'is_authorized': True, 'error': 'Enter title'}
    return render(request, 'ask.html', context=context)


def tag(request, tag_name: str):
    questions = models.Question.objects.get_questions_by_tag(tag_name)
    page, number_of_pages = paginate(questions, request)
    context = {'questions': page, 'tag': tag_name, 'number_of_pages': number_of_pages, 'is_authorized': True}
    return render(request, 'tag.html', context=context)


def hot(request):
    questions = models.Question.objects.all()
    page, number_of_pages = paginate(questions, request)
    context = {'questions': page, 'number_of_pages': number_of_pages, 'is_authorized': True}
    return render(request, 'hot.html', context=context)

