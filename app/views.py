from django.shortcuts import render
from . import models
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from app.forms import LoginForm, RegisterForm, CreateQuestionForm, CreateAnswerForm




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

    context = {'questions': page, 'number_of_pages': number_of_pages, 'is_authorized': request.user.is_authenticated, "user": request.user}
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    question_item, answers = check_question_id(question_id)
    page, number_of_pages = paginate(answers, request)
    context = {'question': question_item[0], 'answers': page, 'number_of_pages': number_of_pages, 'is_authorized': request.user.is_authenticated, "user": request.user, "error":""}

    if (request.method == 'POST'):
        answer_form = CreateAnswerForm(request.POST)

        question = models.Question.objects.get_question_by_id(id=question_id)

        if request.user.id == question.profile_id.id:
            context['error'] = "You can't answer on your question"

            return render(request, 'question.html',  context=context)

        if answer_form.is_valid():
            if (question_id):
                answer = answer_form.save(question=question, user=request.user)

                if answer:
                     return render(request, 'question.html', context=context)

        return render(request, 'question.html', {'error': answer_form.errors})
    

    return render(request, 'question.html', context=context)

@csrf_protect
def login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                dj_login(request, user)

                return redirect(reverse('index'))
            return render(request, 'login.html', {'error': 'Login or/and password are incorrect. Try again.'})
        return render(request, 'login.html', {'error': login_form.errors})

    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    dj_logout(request)
    return redirect(reverse('index'))


def signup(request):
    context = {'is_authorized': request.user.is_authenticated, "user": request.user}

    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    if (request.method == 'POST'):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save()

            if user:
                dj_login(request, user)
                return redirect(reverse('index'))
            register_form.add_error(field=None, error="User saving error!")
        return render(request, 'signup.html', {'error': register_form.errors})

    return render(request, 'signup.html', context=context)

@login_required(login_url='login')
def settings(request):
    context = {'user': request.user, 'is_authorized': request.user.is_authenticated, "user": request.user}
    return render(request, 'settings.html', context=context)

@login_required(login_url='login')
def ask(request):
    context = {'is_authorized': request.user.is_authenticated, "user": request.user}

    if (request.method == 'POST'):
        question_form = CreateQuestionForm(request.POST)

        if question_form.is_valid():
            if (request.user):
                question = question_form.save(request.user)

                if question:
                     return redirect(f'question/{question.id}')

        return render(request, 'ask.html', {'error': question_form.errors})
    

    return render(request, 'ask.html', context=context)


def tag(request, tag_name: str):
    questions = models.Question.objects.get_questions_by_tag(tag_name)
    page, number_of_pages = paginate(questions, request)
    context = {'questions': page, 'tag': tag_name, 'number_of_pages': number_of_pages, 'is_authorized': request.user.is_authenticated, "user": request.user}
    return render(request, 'tag.html', context=context)


def hot(request):
    questions = models.Question.objects.all()
    page, number_of_pages = paginate(questions, request)
    context = {'questions': page, 'number_of_pages': number_of_pages, 'is_authorized': request.user.is_authenticated, "user": request.user}
    return render(request, 'hot.html', context=context)

