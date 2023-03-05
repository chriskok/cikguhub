from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("user_report/", views.user_report, name="user_report"),
    path("expert_report/", views.expert_report, name="expert_report"),
]