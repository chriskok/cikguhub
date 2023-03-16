from django.shortcuts import render
from django.db.models import Case, When
from django.http import HttpResponse
from main.models import *
from sklearn.cluster import KMeans

import json
import numpy as np
import pandas as pd

def index(request):
    return render(request, "recs.html")

def code_user_interests(user_interests):

    skills_code = {'KemahiranMengajar/TeachingSkills' : 'T', 
                  'Bimbingan&Pementoran/Coaching&Mentoring': 'C',
                  'Kepimpinan/Leadership': 'L', 
                  'KemahiranDigital/DigitalSkills(contoh:aplikasiMicrosoftWord/Excel/PowerPointdanGoogleDoc/Sheet/Slide)': 'D',
                  'KemahiranMultimedia/MultimediaSkills(contoh:pembangunanvideo)': 'M'}

    skills = user_interests.split(',')
    coded_skills = []
    for j in range(len(skills)): # look at each skill selected
        s = skills[j].replace(' ', '')
        if s in skills_code.keys():
            skills[j] = s.replace(s, skills_code[s])
        else:
            skills[j] = '*' # for now mark free response with star
        coded_skills.append(skills)
    return coded_skills

def create_user_df(max_track_num, ranking, series_completed, user_interests, user_engagement, cluster_engagement):
    
    df = pd.DataFrame({'Open Tracks': series_completed, 'Max': max_track_num, 'Ranking': ranking, 
                       'Cluster': cluster_engagement, 'User Interest': user_interests, 
                       'User Engagement': user_engagement})
    df['Avaliable'] = [1 if row['Open Tracks'] < row['Max'] else 0 for i, row in df.iterrows()]
    
    return df

def recommend_videos(df):
    
    feature_order = ['Open Tracks', 'User Engagement', 'Cluster', 'Ranking'] # order in which we consider features
    
    avaliable_tracks = df[df['Avaliable'] ==1]
    user_chosen_recs = avaliable_tracks[df['User Interest'] ==1]
    sorted_recs = list(user_chosen_recs.sort_values(feature_order, ascending=False).index)
    
    if len(sorted_recs) == 2:
        return sorted_recs
    elif len(user_chosen_recs) > 2:
        return sorted_recs[0:2]
    else:
        n = 2 - len(sorted_recs)
        other_recs = avaliable_tracks[df['User Interest'] == 0]
        other_recs = list(other_recs.sort_values(feature_order, ascending=False).index)
        return sorted_recs + other_recs[0:n]

# TODO: function to genereate a rec queue for a given user
def produce_recommendations(user):
    user_lm = LearnerModel.objects.get(user=user)
    print(user_lm.school_level)
    # convert to DF ^

    ranking = {'teaching': 0.84, 'coaching': 0.53, 'leadership':0.57, 'digital':0.81, 'multimedia':0.80}
    user_interests = code_user_interests(user_lm.skill_interests)

    # Series for tracks (can count)
    max_track_num = {}  # track: series count (max)
    series_completed = json.loads(user_lm.series_completed) # track: number of series that the user has completed
    all_tracks = Track.objects.all()
    for t in all_tracks:
        max_track_num[t.title] = t.series_set.all().count()
    
    for key,value in max_track_num.items():
        if (key not in series_completed): 
            series_completed[key] = 0

    

def user_recs(request):
    produce_recommendations(request.user)

    recommended_ids = json.loads(RecommendationQueue.objects.get(user=request.user).list_of_ids)
    if len(recommended_ids) > 0:
        recommended_id = recommended_ids[0]
        context = {"series": Series.objects.get(pk=recommended_id)}
    else:
        context = {"series": None}

    return render(request, "recs.html", context=context)

def recommended_module(request, module_id):
    context = {"module": Module.objects.get(pk=module_id)}
    return render(request, "rec_module.html", context=context)

def expert_recs(request, user_id):
    # TODO: add easily swappable modules IF same video
    # TODO: add drag and drop interface for easily switching module order

    # Get the user in question
    if (user_id == 0): curr_user = User.objects.first()
    else: curr_user = User.objects.get(pk=user_id)

    # Get recommended modules, perserving the order of the recommendation list
    list_of_ids = json.loads(RecommendationQueue.objects.get(user=curr_user).list_of_ids)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_of_ids)])
    recommended_series = Series.objects.filter(id__in=list_of_ids).order_by(preserved)

    context = {"series": recommended_series, "curr_user": curr_user, "all_users": User.objects.all()}
    return render(request, "recs_expert.html", context=context)

def user_clustering(request):
    datapoints = [[1, 2], [1, 4], [1, 0], [2, 3], [2, 2], [9, 3], [9, 4], [10, 2], [10, 4], [10, 0]]
    X = np.array(datapoints)
    kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X)

    plotpoints = [{'x': item[0], 'y': item[1]} for item in datapoints]
    context = {
        "learners": LearnerModel.objects.all(),
        "plotpoints": plotpoints,
    }
    return render(request, "user_clustering.html", context=context)
