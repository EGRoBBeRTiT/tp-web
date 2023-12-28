from django import forms
from . import models
from django.contrib.auth.hashers import PBKDF2PasswordHasher


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4)

class RegisterForm(forms.Form):
    nickname = forms.CharField()
    password = forms.CharField(min_length=4)
    passwordRepeat = forms.CharField(min_length=4)
    email = forms.EmailField()
    avatar = forms.CharField(min_length=4, required=False)

    def clean(self):
        password = self.cleaned_data['password']
        passwordRepeat = self.cleaned_data['passwordRepeat']

        if (password != passwordRepeat):
            raise forms.ValidationError('Passwords do not match')
        
    def save(self):
        return models.Profile.objects.create_user(password=self.cleaned_data['password'], email=self.cleaned_data['email'], nickname=self.cleaned_data['nickname'], avatar=self.cleaned_data['avatar'])
    
class CreateQuestionForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(min_length=4)
    tag = forms.CharField(required=False)

    def save(self, user):
        question = models.Question.objects.create(title=self.cleaned_data['title'], text=self.cleaned_data['text'], profile_id=user)


        tags = self.cleaned_data['tag'].split(",")

        for i in range(len(tags)):
            tag = models.Tag.objects.get_tag_by_name(tags[i].strip(" "))

            if tag:
                models.Question.tags.through.objects.create(question_id=question.id, tag_id=tag.id)
            else:
                tag = models.Tag.objects.create(tag=tags[i].strip(" "))

                models.Question.tags.through.objects.create(question_id=question.id, tag_id=tag.id)

        return question
    
class CreateAnswerForm(forms.Form):
    text = forms.CharField(min_length=4)

    def save(self, question, user):
        answer = models.Answer.objects.create(text=self.cleaned_data['text'], question_id=question, profile_id=user)

        return answer




