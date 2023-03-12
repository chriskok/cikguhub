from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib.auth import login, authenticate, logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from .models import *
from django import forms
from django.contrib.messages.views import SuccessMessageMixin


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="main/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("home")

##########################################
#                CREATE                  #
##########################################

# admin.site.register(Video)
# admin.site.register(VideoQuestion)
# admin.site.register(Module)
class VideoCreateView(SuccessMessageMixin, CreateView):
    model = Video
    template_name = 'video_create.html'
    fields = ['title', 'tags', 'description', 'url']
    success_message = 'Video question creation successful!'

    def get_success_url(self):
        return reverse_lazy('main:create_video')
    
class VideoQuestionCreateView(SuccessMessageMixin, CreateView):
    model = VideoQuestion
    template_name = 'video_question_create.html'
    fields = ['video', 'question', 'type', 'possible_answers']
    success_message = 'Video question creation successful!'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['type'] = forms.ChoiceField(widget=forms.RadioSelect, choices=[('OEQ', 'Open-Ended Question (OEQ)'), ('MCQ', 'Multiple Choice Question (MCQ)')])
        return form

    def get_success_url(self):
        return reverse_lazy('main:create_video_question')
    
##########################################
#                UPDATE                  #
##########################################

# class VideoCreateView(SuccessMessageMixin, CreateView):
#     model = Video
#     template_name = 'video_create.html'
#     fields = ['title', 'tags', 'description', 'url']
#     success_message = 'Video question creation successful!'

#     def get_success_url(self):
#         return reverse_lazy('main:create_video')