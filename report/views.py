from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "report.html")

def user_report(request):
    return render(request, "report.html")

def expert_report(request):
    return render(request, "report_expert.html")