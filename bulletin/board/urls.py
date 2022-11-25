from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import AnnounceList, AnnounceDetail, AnnounceCreate, AnnounceUpdate, \
    AnnounceDelete, ReactionList, ReactionCreate, reaction_delete_view, reaction_accept_view, \
    BaseRegisterView, BaseLoginView #, ConformationView,


urlpatterns = [
    path('', AnnounceList.as_view()),
    path('announce_add', AnnounceCreate.as_view()),
    path('announce/<int:pk>', AnnounceDetail.as_view()),
    path('announce/<int:pk>/edit', AnnounceUpdate.as_view()),
    path('reactions', ReactionList.as_view(), name='reactions_list'),
    path('announce/<int:pk>/delete', AnnounceDelete.as_view()),
    path('announce/<int:pk>/react', ReactionCreate.as_view()),
    path('delete/<int:del_id>', reaction_delete_view),
    path('accept/<int:ac_id>', reaction_accept_view),
    path('login/', BaseLoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name = 'signup.html'), name='signup'),
    #path('login/conformation', ConformationView.as_view(template_name = 'login_verification.html'), name='conformation')
]
