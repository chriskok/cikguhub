from django.shortcuts import render
from django.http import HttpResponse
from main.models import *
import datetime
from . import core

def index(request):
    return render(request, "report.html")

def user_report(request):
    curr_learner_model = LearnerModel.objects.get(user=request.user)
    context = {
        'learner_model': curr_learner_model,
        'metrics': {
            m: core.metrics[m].to_view(int(getattr(curr_learner_model, m + "_score")))
            for m in core.metrics
        },
        'description': core.Description(curr_learner_model),
    }
    return render(request, "report.html", context)

def expert_report(request, user_id):
    # TODO: figure out what best to show the expert user to make decisions
    # TODO: maybe we can use AI to generate the summary of feedback first, and have human look over
    # TODO: maybe we can use AI to select the best answers that show growth in specific competencies -> highlight that for experts

    # Get the user in question
    if (user_id == 0): curr_user = User.objects.first()
    else: curr_user = User.objects.get(pk=user_id)

    curr_learner_model = LearnerModel.objects.get(user=curr_user)
    completed_modules = ModuleCompletion.objects.filter(user=curr_user).all()
    context = {
        "learner_model": curr_learner_model, 
        "curr_user": curr_user, 
        "all_users": User.objects.all(),
        "completed_modules": completed_modules,
    }
    return render(request, "report_expert.html", context)