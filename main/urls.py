from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

app_name = "main"

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),

    # Create
    path("create_video", login_required(views.VideoCreateView.as_view()), name= "create_video"),
    path("create_video_question", login_required(views.VideoQuestionCreateView.as_view()), name= "create_video_question"),

    # Update
]