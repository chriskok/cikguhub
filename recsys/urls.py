from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("recs/", views.user_recs, name="user_recs"),
    path("expert_recs/", views.expert_recs, name="expert_recs"),
]