from django.shortcuts import render
from django.http import HttpResponse
from main.models import *

def index(request):
    return render(request, "report.html")

def user_report(request):
    curr_learner_model = LearnerModel.objects.get(user=request.user)
    context = {
        'learner_model': curr_learner_model,
        'planner_score': int(curr_learner_model.planner_score),
        'guardian_score': int(curr_learner_model.guardian_score),
        'mentor_score': int(curr_learner_model.mentor_score),
        'motivator_score': int(curr_learner_model.motivator_score),
        'assessor_score': int(curr_learner_model.assessor_score),
    }
    return render(request, "report.html", context)

def expert_report(request, user_id):
    # Get the user in question
    if (user_id == 0): curr_user = User.objects.first()
    else: curr_user = User.objects.get(pk=user_id)

    print("HELKERKJDWA")
    curr_learner_model = LearnerModel.objects.get(user=curr_user)

    context = {"learner_model": curr_learner_model, "curr_user": curr_user, "all_users": User.objects.all()}
    return render(request, "report_expert.html", context)