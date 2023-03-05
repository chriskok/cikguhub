from django.shortcuts import render
from django.http import HttpResponse
from main.models import *
import json

def index(request):
    return render(request, "recs.html")

def user_recs(request):
    recommended_module_ids = json.loads(RecommendationQueue.objects.get(user=request.user).list_of_module_ids)
    if len(recommended_module_ids) > 0:
        recommended_module_id = recommended_module_ids[0]
        context = {"module": Module.objects.get(pk=recommended_module_id)}
    else:
        context = {"module": None}

    return render(request, "recs.html", context=context)

def expert_recs(request, user_id):
    if (user_id == 0): curr_user = User.objects.first()
    else: curr_user = User.objects.get(pk=user_id)

    recommended_modules = Module.objects.filter(id__in=json.loads(RecommendationQueue.objects.get(user=curr_user).list_of_module_ids))
    context = {"module": recommended_modules, "curr_user": curr_user, "all_users": User.objects.all()}
    return render(request, "recs_expert.html", context=context)