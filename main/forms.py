from django import forms
from main.models import MyUser, Post
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="пароль (повторно)", widget=forms.PasswordInput)
    username = forms.CharField(label="никнейм", help_text='')

    class Meta:
        model = MyUser
        fields = ('username', 'password', 'password_confirm', 'avatar', 'bio')
        labels = {'username': 'никнейм', 'password': 'пароль', 'password_confirm': 'пароль (повторно)', 'avatar': 'аватарка', 'bio': 'расскажите о себе'}

        error_messages = {
            'username': {
                'unique': "пользователь с таким логином уже зарегистрирован",
            },
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and not re.fullmatch(r"^[a-zA-z-]+$", username):
            raise forms.ValidationError("логин должен содержать только латиницу и дефисы")
        return username

    def clean(self):
        super().clean()
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            raise ValidationError({'password_confirm': 'пароли не совпадают'})
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(label="никнейм", help_text='')
    class Meta:
        model = MyUser
        fields = ('username', 'avatar', 'bio')
        labels = {'username': 'никнейм', 'avatar': 'аватарка', 'bio': 'расскажите о себе'}


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_content']
        labels = {'post_content': 'содержание поста'}


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_content']
        labels = {'post_content': 'содержание поста'}

class CommentForm(forms.Form):
    comment_text = forms.CharField(required=True, label="комментарий")
    def clean(self):
        cleaned_data = super().clean()
        comment_text = cleaned_data.get('comment_text')
        return cleaned_data