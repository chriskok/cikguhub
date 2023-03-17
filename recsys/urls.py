from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("recs/", login_required(views.user_recs), name="user_recs"),
    path("recommended_module/<int:module_id>/", login_required(views.recommended_module), name="recommended_module"),
    path("expert_recs/<int:user_id>/", login_required(views.expert_recs), name="expert_recs"),
    path("user_clustering/", login_required(views.user_clustering), name="user_clustering"),
]