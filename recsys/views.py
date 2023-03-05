from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "recs.html")

def user_recs(request):
    return render(request, "recs.html")

def expert_recs(request):
    return render(request, "recs_expert.html")