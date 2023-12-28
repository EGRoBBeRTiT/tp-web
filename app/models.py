from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import PBKDF2PasswordHasher


class ProfileManager(BaseUserManager):
    def get_user_by_username(self, username):
        return self.filter(username=username)

    def get_best_members(self):
        return self.filter(id__lt=6)
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='uploads/')
    nickname = models.CharField(max_length=20, unique=True)
    question_likes = models.ManyToOneRel(field = "question_likes", field_name = "question_likes", to = "profile_id")
    answer_likes = models.ManyToOneRel(field = "answer_likes", field_name = "answer_likes", to = "profile_id")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'nickname'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']

    objects = ProfileManager()


class TagManager(models.Manager):
    def get_popular_tags(self):
        return self.filter(id__lt=9)
    
    def get_tag_by_name(self, tag):
        tags = self.filter(tag=tag)

        if len(tags):
            return tags[0]
        
        return tags


class Tag(models.Model):
    tag = models.CharField(max_length=30)

    objects = TagManager()

    def __str__(self):
        return self.tag


class QuestionManager(models.Manager):
    def get_hot_questions(self):
        return self.order_by('-likes__amount_of_likes')

    def get_new_questions(self):
        return self.order_by('-date_of_creation')

    def get_questions_by_tag(self, tag):
        return self.filter(tags__tag=tag)
    
    def get_question_by_id(self, id):
        questions = self.filter(id=id)

        if len(questions):
            return questions[0]
        
        return questions
    
class QuestionLike(models.Model):
    date_of_creation = models.DateTimeField(auto_now_add=True)
    is_like = models.BooleanField(default=False)
    profile_id = models.ForeignKey('Profile', related_name= 'question_likes', on_delete = models.CASCADE)
    question_id = models.ForeignKey('Question', related_name= 'question_likes', on_delete = models.CASCADE)

    class Meta:
        ordering = ['-id']
        unique_together = ('profile_id', 'question_id')


class Question(models.Model):
    title = models.CharField(max_length=90)
    text = models.TextField(max_length=512)
    profile_id = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    amount_of_answers = models.IntegerField(default=0)
    question_likes = models.ManyToOneRel(field = "question_likes", field_name = "question_likes", to = "question_id")
    answers = models.ManyToOneRel(field = "answers", field_name = "answers", to = "question_id")

    objects = QuestionManager()

    class Meta:
        ordering = ['-id']


class AnswerLike(models.Model):
    date_of_creation = models.DateTimeField(auto_now_add=True)
    is_like = models.BooleanField(default=False)
    profile_id = models.ForeignKey('Profile', related_name= 'answer_likes', on_delete = models.CASCADE)
    answer_id = models.ForeignKey('Answer', related_name= 'answer_likes', on_delete = models.CASCADE)

    class Meta:
        ordering = ['-id']
        unique_together = ('profile_id', 'answer_id')

class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=512)
    profile_id = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    answer_likes = models.ManyToOneRel(field = "answer_likes", field_name = "answer_likes", to = "answer_id")
    question_id = models.ForeignKey('Question', related_name='answers', on_delete = models.CASCADE)

    class Meta:
        ordering = ['-id']

