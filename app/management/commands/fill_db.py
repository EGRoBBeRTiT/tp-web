from django.core.management.base import BaseCommand
from datetime import datetime
from random import randint
from app import models


class Command(BaseCommand):
    help = 'Command manager to fill database'

    def handle(self, *args, **options):
        ratio = options['ratio']

        profile_count = ratio + 1
        questions_count = ratio * 10 + 1
        answers_count = ratio * 100 + 1
        tags_count = ratio + 1
        likes_count = ratio * 200 + 1

        # users_for_create = [
        #     models.Profile(
        #         username=f'user-{i}',
        #         password=f'user-{i}',
        #         first_name=f'name of user-{i}',
        #         last_name=f'surname of user-{i}',
        #         email=f'user.{i}@google.com',
        #         is_staff=False,
        #         is_active=True,
        #         avatar=f'{randint(1, 20)}.jpg',
        #         nickname=f'robber.{i}'
        #     ) for i in range(profile_count)
        # ]
        # models.Profile.objects.bulk_create(users_for_create)

        users = models.Profile.objects.all()

        # tags_for_create = [
        #     models.Tag(
        #         tag=f'tag [{i}]',
        #     ) for i in range(tags_count)
        # ]
        # models.Tag.objects.bulk_create(tags_for_create)


        # questions_for_create = [
        #     models.Question(
        #         title=f'Title of question {i}',
        #         text=f'Text of question {i}',
        #         profile_id=users[randint(0, profile_count - 1)],
        #     ) for i in range(questions_count)
        # ]
        # models.Question.objects.bulk_create(questions_for_create)

        # question_tag = []
        # for i in range(questions_count):
        #     amount_of_tags = randint(0, 11)
        #     unicum_arr =[]

        #     for j in range(amount_of_tags):
        #         index = randint(1, tags_count)

        #         if not (index in unicum_arr):
        #             unicum_arr.append(index)
        #             question_tag.append(
        #             models.Question.tags.through(
        #                 question_id=i + 1,
        #                 tag_id=index
        #             )
        #         )

        # models.Question.tags.through.objects.bulk_create(question_tag)

        questions = models.Question.objects.all()
        answers_for_create = []
        for i in range(answers_count):
            question_id = randint(0, questions_count - 1)
            answers_for_create.append(
                models.Answer(
                    question_id=questions[questions_count - 1 - question_id],
                    text=f'text of answer {i}',
                    profile_id=users[randint(0, profile_count - 1)],
                    is_correct=True if randint(0, 1) else False,
                )
            )
            questions.filter(id=question_id + 1).update(amount_of_answers=questions[questions_count - 1 - question_id].amount_of_answers + 1)
        models.Answer.objects.bulk_create(answers_for_create)

        likes_for_create = [
            models.QuestionLike(
                is_like=True if randint(0, 1) else False,
                profile_id=users[randint(0, profile_count - 1)],
                question_id=questions[randint(0, questions_count - 1)]
            ) for i in range(likes_count // 2)
        ]
        models.QuestionLike.objects.bulk_create(likes_for_create)

        answers = models.Answer.objects.all()

        likes_for_create = [
            models.AnswerLike(
                is_like=True if randint(0, 1) else False,
                profile_id=users[randint(0, profile_count - 1)],
                answer_id=answers[randint(0, answers_count - 1)]
            ) for i in range(likes_count // 2)
        ]
        models.AnswerLike.objects.bulk_create(likes_for_create)


    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)
