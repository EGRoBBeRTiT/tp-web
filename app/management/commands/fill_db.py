from django.core.management.base import BaseCommand
from datetime import datetime
from random import randint
from app import models
from itertools import islice


class Command(BaseCommand):
    help = 'Command manager to fill database'

    def handle(self, *args, **options):
        ratio = options['ratio']


        profile_count = ratio + 1
        questions_count = ratio * 10 + 1
        answers_count = ratio * 100 + 1
        tags_count = ratio + 1
        likes_count = ratio * 200 + 1

        batch_size = 1000

        def generate_users(): 
            for i in range(profile_count):
                print(f'{int(100 * (i / profile_count))}%', f'{i}/{profile_count}', '-', 'Users')

                yield models.Profile(
                    username=f'user-{i}',
                    password=f'user-{i}',
                    first_name=f'name of user-{i}',
                    last_name=f'surname of user-{i}',
                    email=f'user.{i}@google.com',
                    is_staff=False,
                    is_active=True,
                    avatar=f'{randint(1, 20)}.jpg',
                    nickname=f'robber.{i}'
                )
        models.Profile.objects.bulk_create(list(generate_users()), batch_size=batch_size) 
        
        def generate_tags(): 
            for i in range(tags_count):
                print(f'{int(100 * (i / tags_count))}%', f'{i}/{tags_count}', '-', 'Tags')
                yield models.Tag(
                tag=f'tag [{i}]',
            )
        models.Tag.objects.bulk_create(list(generate_tags()), batch_size=batch_size) 

        def generate_questions(): 
            for i in range(questions_count):
                print(f'{int(100 * (i / questions_count))}%', f'{i}/{questions_count}', '-', 'Questions')
                yield models.Question(
                title=f'Title of question {i}',
                text=f'Text of question {i}',
                profile_id_id=randint(1, profile_count),
            )
        models.Question.objects.bulk_create(list(generate_questions()), batch_size=batch_size) 

        def generate_question_tags(): 
            for i in range(questions_count):
                amount_of_tags = randint(0, 11)
                unicum_arr =[]

                for j in range(amount_of_tags):
                    index = randint(1, tags_count)

                    if not (index in unicum_arr):
                        print(f'{int(100 * ((i + j) / (questions_count * 10)))}%', f'{(i + j)}/{(questions_count * 10)}', '-', 'Question Tags')
                        unicum_arr.append(index)
                        yield models.Question.tags.through(
                            question_id=i + 1,
                            tag_id=index
                        )
        models.Question.tags.through.objects.bulk_create(list(generate_question_tags()), batch_size=batch_size) 

   
        def generate_answers():
            for i in range(answers_count):
                print(f'{int(100 * (i / answers_count))}%', f'{i}/{answers_count}', '-', 'Answers')

                question_id = randint(0, questions_count - 1)

                yield models.Answer(
                        question_id_id=questions_count - question_id,
                        text=f'text of answer {i}',
                        profile_id_id=randint(1, profile_count),
                        is_correct=True if randint(0, 1) else False,
                    )
        models.Answer.objects.bulk_create(list(generate_answers()), batch_size=batch_size) 

        def generate_question_likes():
            keys = [[] for i in range(profile_count)]

            for i in range(likes_count // 2):
                profile_id = randint(1, profile_count)
                question_id = randint(1, questions_count)

                if (question_id in keys[profile_id - 1]):
                    while (question_id in keys[profile_id - 1]):
                        question_id = randint(1, questions_count)
                    keys[profile_id - 1].append(question_id)
                else:
                    keys[profile_id - 1].append(question_id)  

                print(f'{int(100 * (i / (likes_count // 2)))}%', f'{i}/{(likes_count // 2)}', '-', 'Question Likes')                  
                
                yield models.QuestionLike(
                is_like=True if randint(0, 1) else False,
                profile_id_id=profile_id,
                question_id_id=question_id
            )
        models.QuestionLike.objects.bulk_create(list(generate_question_likes()), batch_size=batch_size) 

        def generate_answer_likes():
            keys = [[] for i in range(profile_count)]

            for i in range(likes_count // 2):
                profile_id = randint(1, profile_count)
                answer_id = randint(1, answers_count)

                if (answer_id in keys[profile_id - 1]):
                    while (answer_id in keys[profile_id - 1]):
                        answer_id = randint(1, questions_count)
                    keys[profile_id - 1].append(answer_id)
                else:
                    keys[profile_id - 1].append(answer_id) 

                print(f'{int(100 * (i / (likes_count // 2)))}%', f'{i}/{(likes_count // 2)}', '-', 'Answers Likes')       

                yield models.AnswerLike(
                is_like=True if randint(0, 1) else False,
                profile_id_id=profile_id,
                answer_id_id=answer_id
            )
        models.AnswerLike.objects.bulk_create(list(generate_answer_likes()), batch_size=batch_size) 

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)
