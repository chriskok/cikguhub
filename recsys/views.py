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

def expert_recs(request):
    recommended_modules = Module.objects.filter(id__in=json.loads(RecommendationQueue.objects.get(user=request.user).list_of_module_ids))
    context = {"module": recommended_modules}
    return render(request, "recs_expert.html", context=context)