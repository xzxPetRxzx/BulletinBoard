from random import randint

import requests
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView
from requests import request


from .filters import ReactionFilter
from .models import Announce, User, Reaction, OneTimeCode
from .forms import AnnounceForm, ReactionForm, LoginForm, BaseRegisterForm, BaseLoginForm#, LoginConformationForm
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError


class AnnounceList(ListView):
    model = Announce
    context_object_name = 'announces'
    template_name = 'announce_list.html'
    ordering = '-creation_date'
    paginate_by = 10


class AnnounceDetail(DetailView):
    model = Announce
    context_object_name = 'cur_announce'
    template_name = 'announce.html'


class ReactionList(LoginRequiredMixin, ListView):
    model = Reaction
    context_object_name = 'reactions'
    template_name = 'reaction_list.html'
    ordering = '-creation_date'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cur_user = self.request.user
        reaction_for_user = Reaction.objects.filter(announce__author=cur_user)
        context['filter'] = ReactionFilter(self.request.GET, queryset=reaction_for_user)
        return context


class AnnounceCreate(LoginRequiredMixin, CreateView):
    template_name = 'announce_add.html'
    form_class = AnnounceForm
    success_url = '/board/'

    def form_valid(self, form):
        ann_model = form.save(commit=False)
        ann_model.author = self.request.user
        ann_model.save()
        return super().form_valid(form)


class AnnounceUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'announce_add.html'
    form_class = AnnounceForm
    success_url = '/board/'

    def get_object(self, **kwargs):
        ann_id = self.kwargs.get('pk')
        return Announce.objects.get(pk=ann_id)


class AnnounceDelete(LoginRequiredMixin, DeleteView):
    template_name = 'announce_delete.html'
    queryset = Announce.objects.all()
    success_url = '/board/'


class ReactionCreate(LoginRequiredMixin, CreateView):
    template_name = 'announce_add.html'
    form_class = ReactionForm
    success_url = '/board/'

    def form_valid(self, form):
        react_model = form.save(commit=False)
        react_model.author = self.request.user
        pk = self.kwargs['pk']
        react_model.announce_id = pk
        return super().form_valid(form)


def reaction_delete_view(del_id):
    del_reaction = Reaction.objects.get(id=del_id)
    del_reaction.delete()
    return HttpResponseRedirect(reverse('reactions_list'))


def reaction_accept_view(ac_id):
    ac_reaction = Reaction.objects.get(id=ac_id)
    ac_reaction.accepted = True
    ac_reaction.save()
    return HttpResponseRedirect(reverse('reactions_list'))


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/board/login/'


class BaseLoginView(LoginView):
    form_class = BaseLoginForm

    #def form_valid(self, form):
     #   OneTimeCode.objects.create(code=randint(100000, 999999), user=form.get_user())
      #  return HttpResponseRedirect('/board/login/conformation')


#class ConformationView(FormView):
#    form_class = LoginConformationForm
#
#    def form_valid(self, form):
#
 #       if OneTimeCode.objects.filter(code=form.cleaned_data['code'],user__username=form.cleaned_data['username']).exists():
  #          user = User.objects.get(username=form.cleaned_data['username'])
   #         OneTimeCode.objects.get(code=form.cleaned_data['code']).delete()
    #        login(request=request, user=user.id)
     #       return HttpResponseRedirect('/board/')
      #  else:
       #     return HttpResponseRedirect('/board/login/conformation')
