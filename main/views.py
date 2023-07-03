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
import random

exp_level_conversion = {
    'Kurang daripada 1 tahun / Less than 1 year': 0.5,
    '1 hingga 5 tahun / 1 to 5 years': 3.0,
    '6 hingga 10 tahun / 6 to 10 years': 8.0,
    'Lebih daripada 10 tahun / More than 10 years': 12.5,
}

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create new learner model object
            years_of_experience = exp_level_conversion[form.cleaned_data['years_of_experience']]
            percentage_of_experience = years_of_experience/12.5*100
            planner_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20)))
            guardian_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20)))
            mentor_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20)))
            motivator_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20)))
            assessor_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20)))

            try:
                lm, created = LearnerModel.objects.get_or_create(user=user, 
                    full_name=form.cleaned_data['full_name'],
                    school = form.cleaned_data['school'],
                    school_level = form.cleaned_data['school_level'],
                    years_of_experience = years_of_experience,
                    role = ','.join(form.cleaned_data['role']),
                    skill_interests = ','.join(form.cleaned_data['skill_interests']),
                    planner_score = planner_score,
                    guardian_score = guardian_score,
                    mentor_score = mentor_score,
                    motivator_score = motivator_score,
                    assessor_score = assessor_score,
                    current_feedback = Feedback.objects.create(user=user, feedback="",
                        planner_score = planner_score,
                        guardian_score = guardian_score,
                        mentor_score = mentor_score,
                        motivator_score = motivator_score,
                        assessor_score = assessor_score,
                    )
                )
                if (created): print(f'LearnerModel: {lm.full_name} created')
            except Exception as e:
                print(f'Failed to create LearnerModel for: {user}, ERROR: {e}')
                
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/recsys/recs/")
        messages.error(request, f"Unsuccessful registration: {[(field, errors[0]) for field, errors in form.errors.items()]}")
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
                if (request.GET.get('next')): return redirect(request.GET.get('next'))
                else:
                    return redirect("/recsys/recs/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    
    return render(request=request, template_name="main/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("/main/login")

##########################################
#                CREATE                  #
##########################################

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

class ModuleCreateView(SuccessMessageMixin, CreateView):
    model = Module
    template_name = 'module_create.html'
    fields = ['video', 'questions', 'title']
    success_message = 'Module creation successful!'

    def get_success_url(self):
        return reverse_lazy('main:create_module')
    
    
##########################################
#                UPDATE                  #
##########################################

class ModuleUpdateView(SuccessMessageMixin, UpdateView):
    model = Module
    fields = ['video', 'questions', 'title']
    template_name = 'module_update.html'
    success_message = 'Module updated successfully!'

    def get_success_url(self):
        return reverse_lazy('recsys:expert_recs', kwargs={'user_id': 0})

    def get_form(self, *args, **kwargs):
        form = super(ModuleUpdateView, self).get_form(*args, **kwargs)
        form.fields['questions'].queryset = VideoQuestion.objects.filter(video=self.object.video)
        # form.fields['b_a'].queryset = A.objects.filter(a_user=self.request.user) 
        return form