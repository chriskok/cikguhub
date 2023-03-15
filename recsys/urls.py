from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("recs/", views.user_recs, name="user_recs"),
    path("recommended_module/<int:module_id>/", views.recommended_module, name="recommended_module"),
    path("expert_recs/<int:user_id>/", views.expert_recs, name="expert_recs"),
    path("user_clustering/", views.user_clustering, name="user_clustering"),
]