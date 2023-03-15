from django.shortcuts import render
from django.db.models import Case, When
from django.http import HttpResponse
from main.models import *
from sklearn.cluster import KMeans

import json
import numpy as np

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
    # TODO: add easily swappable modules IF same video
    # TODO: add drag and drop interface for easily switching module order

    # Get the user in question
    if (user_id == 0): curr_user = User.objects.first()
    else: curr_user = User.objects.get(pk=user_id)

    # Get recommended modules, perserving the order of the recommendation list
    list_of_module_ids = json.loads(RecommendationQueue.objects.get(user=curr_user).list_of_module_ids)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_of_module_ids)])
    recommended_modules = Module.objects.filter(id__in=list_of_module_ids).order_by(preserved)

    context = {"modules": recommended_modules, "curr_user": curr_user, "all_users": User.objects.all()}
    return render(request, "recs_expert.html", context=context)

def user_clustering(request):
    datapoints = [[1, 2], [1, 4], [1, 0], [2, 3], [2, 2], [9, 3], [9, 4], [10, 2], [10, 4], [10, 0]]
    X = np.array(datapoints)
    kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X)

    plotpoints = [{'x': item[0], 'y': item[1]} for item in datapoints]
    context = {
        "learners": LearnerModel.objects.all(),
        "plotpoints": plotpoints,
    }
    return render(request, "user_clustering.html", context=context)