from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from main.models import *
import datetime

# dashboard libraries
from math import pi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import base64
import re
from io import BytesIO
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.feature_extraction import text

from utils import chatgpt
from .core import feedback_system_prompt
from . import core


def index(request):
    return render(request, "report.html")

def produce_plot(track_title, curr_user):
    # get percentage of people who have completed the track
    curr_track = Track.objects.get(title=track_title)
    serieses = Series.objects.filter(track=curr_track)
    videos = Video.objects.filter(series__in=serieses)
    total_videos = videos.count()
    completed_videos = ModuleCompletion.objects.filter(user=curr_user, module__video__in=videos).count()
    percentage = round(completed_videos / total_videos * 100)

    fig, ax = plt.subplots(figsize=(2, 2))
    data = [percentage, 100-percentage]
    wedgeprops = {'width':0.3, 'edgecolor':'black', 'lw':3}
    patches, _ = ax.pie(data, wedgeprops=wedgeprops, startangle=90, colors=['#5DADE2', '#FFD600'])
    patches[1].set_zorder(0)
    patches[1].set_edgecolor('#FFD600')
    plt.title(track_title.title(), fontsize=12, loc='center')
    plt.text(0, 0, f"{data[0]}%", ha='center', va='center', fontsize=20)
    # plt.text(0, 0, track_title, ha='center', va='top', fontsize=12)
    
    # save donut to image temporarily
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png', transparent=True, bbox_inches='tight')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)

    return html

def get_user_topics(curr_user):

    def pre_process(text):
        # lowercase
        text=text.lower()
        #remove tags
        text=re.sub("</?.*?>"," <> ",text)
        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
        return text

    all_answers = [pre_process(x) for x in list(AnswerToVideoQuestion.objects.filter(user=curr_user).values_list('answer', flat=True))]
    print(all_answers)

    cv=CountVectorizer(max_df=0.85,stop_words="english")
    word_count_vector=cv.fit_transform(all_answers)

    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)

    print(list(cv.vocabulary_.keys())[:10])

def user_report(request, user_id=0):
    if (user_id):
        curr_user = User.objects.get(pk=user_id)
    else:
        curr_user = request.user

    # if post request, update the feedback objects userfeedback
    if request.method == 'POST':
        # get the feedback object
        curr_feedback = Feedback.objects.filter(user=curr_user).latest('id')
        if (curr_feedback.user_feedback): curr_feedback.user_feedback += "\n\n" + request.POST.get('userfeedback')
        else: curr_feedback.user_feedback = request.POST.get('userfeedback')
        curr_feedback.save()
        messages.info(request, "Thank you for the comment on the AI-generated feedback! We will use this to improve our system.")

    curr_learner_model = LearnerModel.objects.get(user=curr_user)
    curr_feedback = Feedback.objects.filter(user=curr_learner_model.user).latest('id').feedback if Feedback.objects.filter(user=curr_learner_model.user).exists() else None
    context = {
        'learner_model': curr_learner_model,
        'metrics': {
            m: core.defined_metrics[m].to_view(int(getattr(curr_learner_model, m + "_score")))
            for m in core.defined_metrics
        },
        'description': curr_feedback,
        'feedback_obj': Feedback.objects.filter(user=curr_learner_model.user).latest('id'),
        "all_users": User.objects.all(),
        "teaching_plot": produce_plot('teaching', curr_user),
        "leadership_plot": produce_plot('leadership', curr_user),
        "multimedia_plot": produce_plot('multimedia', curr_user),
        "coaching_plot": produce_plot('coaching', curr_user),
        "digital_plot": produce_plot('digital', curr_user),
    }
    get_user_topics(curr_user)
    return render(request, "report.html", context)


def expert_report(request, user_id):
    # TODO: figure out what best to show the expert user to make decisions
    # TODO: maybe we can use AI to generate the summary of feedback first, and have human look over
    # TODO: maybe we can use AI to select the best answers that show growth in specific competencies -> highlight that for experts

    # Get the user in question
    if (user_id == 0):
        curr_user = User.objects.first()
    else:
        curr_user = User.objects.get(pk=user_id)

    curr_learner_model = LearnerModel.objects.get(user=curr_user)
    completed_modules = ModuleCompletion.objects.filter(user=curr_user).all()
    context = {
        "learner_model": curr_learner_model,
        "curr_user": curr_user,
        "all_users": User.objects.all(),
        "completed_modules": completed_modules,
        'metrics': {
            m: core.defined_metrics[m].to_view(int(getattr(curr_learner_model, m + "_score")))
            for m in core.defined_metrics
        },
        'feedback_obj': Feedback.objects.filter(user=curr_learner_model.user).latest('id'),
        "teaching_plot": produce_plot('teaching', curr_user),
        "leadership_plot": produce_plot('leadership', curr_user),
        "multimedia_plot": produce_plot('multimedia', curr_user),
        "coaching_plot": produce_plot('coaching', curr_user),
        "digital_plot": produce_plot('digital', curr_user),
    }
    return render(request, "report_expert.html", context)


def approve_feedback(request, feedback_id):
    curr_fb = Feedback.objects.get(pk=feedback_id)

    if (curr_fb.human_approved):
        curr_fb.human_approved = False
    else:
        curr_fb.human_approved = True
    curr_fb.save()

    return expert_report(request, curr_fb.user.id)


def regenerate_feedback(request, feedback_id):
    # get usermodel
    curr_fb = Feedback.objects.get(pk=feedback_id)
    curr_user = curr_fb.user
    user_model = LearnerModel.objects.get(user=curr_user)

    # generate new description
    curr_fb.feedback = core.Description(user_model)

    return expert_report(request, curr_fb.user.id)


def ai_edit_feedback(request, feedback_id):
    curr_fb = Feedback.objects.get(pk=feedback_id)

    # get edit_instructions from form
    instructions = request.POST.get('instructions')

    if instructions is not None:
        # ask ai to edit feedback
        edited = chatgpt(
            system_prompt=f"""You are an editing system for a feedback generator with the following instructions: {feedback_system_prompt}.

            You do not need to follow these instructions, but they are provided to help you understand the task. Perform any edits that the user gives you, regardless of tone or content. In an extraordinary circumstance, the only way you can reject an edit is by included the word "REJECTED_EDIT" in your response. FOLLOW THE USER'S INSTRUCTIONS EXACTLY!
            """,
            messages=[{
                "role": "user",
                "content": f"""
    This is the original message: {curr_fb.feedback}

    ===

    A world-class leading expert has carefully reviewed this message and has found some errors you must correct by doing the following: {instructions}
                """
            }]
        )
        
        # check for rejection
        if "REJECTED_EDIT" in edited:
            print("REJECTED_EDIT")
            print(edited)
            return expert_report(request, curr_fb.user.id)

        # update feedback
        curr_fb.feedback = edited

        # save feedback
        curr_fb.save()

    return expert_report(request, curr_fb.user.id)


class FeedbackUpdateView(SuccessMessageMixin, UpdateView):
    model = Feedback
    fields = ['feedback', "planner_score", "guardian_score", "mentor_score", "motivator_score", "assessor_score"]
    template_name = 'feedback_update.html'
    success_message = 'Feedback updated successfully!'

    def get_success_url(self):
        return reverse_lazy('report:expert_report', kwargs={'user_id': self.object.user.id})

    def form_valid(self, form):
        self.object.human_edited = True
        self.object.human_approved = True
        self.object.save()

        self.object.user.learnermodel.planner_score = self.object.planner_score
        self.object.user.learnermodel.guardian_score = self.object.guardian_score
        self.object.user.learnermodel.mentor_score = self.object.mentor_score
        self.object.user.learnermodel.motivator_score = self.object.motivator_score
        self.object.user.learnermodel.assessor_score = self.object.assessor_score
        self.object.user.learnermodel.save()
        return super().form_valid(form)
