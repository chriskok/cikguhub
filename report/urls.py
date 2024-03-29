from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("user_report/", login_required(views.user_report), name="user_report"),
    path("user_report/<int:user_id>/", login_required(views.user_report), name="user_report"),
    path("expert_report/<int:user_id>/", login_required(views.expert_report), name="expert_report"),
    path("school_report/", login_required(views.school_report), name="school_report"),
    path("update_feedback/<pk>", login_required(views.FeedbackUpdateView.as_view()), name="update_feedback"),
    path("approve_feedback/<int:feedback_id>", login_required(views.approve_feedback), name="approve_feedback"),
    path("regenerate_feedback/<int:feedback_id>", login_required(views.regenerate_feedback), name="regenerate_feedback"),
    path("ai_edit_feedback/<int:feedback_id>", login_required(views.ai_edit_feedback), name="ai_edit_feedback"),
]