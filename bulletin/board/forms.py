import requests
from allauth.account.forms import LoginForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth import login
from django.forms import ModelForm, HiddenInput, CharField, EmailField, PasswordInput, Form
from django.http import HttpResponseRedirect
import requests

from .models import Announce, Reaction, User, OneTimeCode
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError


class AnnounceForm(ModelForm):
    # content = RichTextUploadingField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Announce
        fields = ('heading', 'content', 'category')
        labels = dict(heading=('Заголовок'), content=('Содержание'), category=('Категория'))


class ReactionForm(ModelForm):
    class Meta:
        model = Reaction
        fields = ['content', ]


class BaseRegisterForm(UserCreationForm):
    username = CharField(label='Имя пользователя', min_length=5, max_length=150)
    email = EmailField(label='Email')
    password1 = CharField(label='Пароль', widget=PasswordInput)
    password2 = CharField(label='Подтверждение пароля', widget=PasswordInput)
    code = CharField(label='код доступа', widget=PasswordInput)


class BaseLoginForm(AuthenticationForm):
    username = CharField(label='Имя пользователя', max_length=150)
    password = CharField(label='Пароль', widget=PasswordInput)


#class LoginConformationForm(Form):
 #   username = CharField(label='Имя пользователя', max_length=150)
  #  code = CharField(label='Код верификации', max_length=6, widget=PasswordInput)

