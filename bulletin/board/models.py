from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.shortcuts import redirect
from requests import request


class Announce(models.Model):
    CATEGORY_CHOICES = (
        ('Танк', 'Танк'), ('Хил', 'Хил'), ('ДД', 'ДД'), ('Гилдмастер', 'Гилдмастер'),
        ('Квестгивер', 'Квестгивер'), ('Кузнец', 'Кузнец'), ('Кожевник', 'Кожевник'),
        ('Зельевар', 'Зельевар'), ('МЗ', 'Мастер заклинаний')
    )
    heading = models.CharField(max_length=255)
    content = RichTextUploadingField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f'/board/announce/{self.id}'


class Reaction(models.Model):
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE)

    #def get_absolute_url(self):
        #return f'/board/reaction/{self.id}'


class OneTimeCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)