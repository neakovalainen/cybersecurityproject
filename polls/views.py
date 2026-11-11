from django.db.models import F
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question, Account
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    if request.user.is_authenticated:
      account = Account.objects.get(owner=request.user)
    else:
      account = None
    context = {
      "latest_question_list": latest_question_list,
      "account": account,
    }
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

@login_required
def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST["choice"])
  except (KeyError, Choice.DoesNotExist):
    return render(
      request,
      "polls/detail.html",
      {
        "question": question,
        "error_message": "You didn't select a choice.",
      },
    )
  else:
    selected_choice.votes = F("votes") + 1
    account = Account.objects.get(owner=request.user)
    account.times_voted += 1
    account.save()
    selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def create_user(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      Account.objects.create(owner=user)
      return redirect("/polls/login")
  else:
    form = UserCreationForm()

  return render(request, "polls/create_user.html", {"form": form})

def loginPage(request):
  return render(request, 'polls/login.html')