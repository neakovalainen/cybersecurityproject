from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", LoginView.as_view(template_name='polls/login.html'), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("create_user", views.create_user, name="create_user"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote")
]