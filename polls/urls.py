from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", LoginView.as_view(template_name='polls/login.html')),
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]