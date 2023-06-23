from django.shortcuts import  render, redirect
from django.db.models import Case, When
from django.http import HttpResponse
from django.contrib import messages
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering

from .forms import *
from main.models import *
from report import core

import json
import asyncio
import threading
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot

def index(request):
    return render(request, "recs.html")

################################
#       DATA MANIPULATION      #
################################

skills_code = {'KemahiranMengajar/TeachingSkills' : 'teaching', 
              'Bimbingan&Pementoran/Coaching&Mentoring': 'coaching',
              'Kepimpinan/Leadership': 'leadership', 
              'KemahiranDigital/DigitalSkills(contoh:aplikasiMicrosoftWord/Excel/PowerPointdanGoogleDoc/Sheet/Slide)': 'digital',
              'KemahiranMultimedia/MultimediaSkills(contoh:pembangunanvideo)': 'multimedia'}

exp_code = {'Kurang daripada 1 tahun / Less than 1 year': 0,
            '1 hingga 5 tahun / 1 to 5 years' : 1,
            '6 hingga 10 tahun / 6 to 10 years': 2,
           'Lebih daripada 10 tahun / More than 10 years': 3}

role_code = {'GuruAkademikBiasa/AcademicTeacher': 'T', 
             'KetuaPanitia/PanelHead': 'P', 
             'Officer': 'O'}

level_code = {'Other:': -1,
              'Other': -1,
              'Saya bukan seorang cikgu / I am not a teacher': 0,
              'Sekolah Kebangsaan / National Primary School': 1,
              'Sekolah Menengah Kebangsaan / National Secondary School': 2}

def code_responses(df):

    coded_exp = []
    coded_skills = []
    coded_roles = []
    coded_level = []

    for i, col in df.iterrows(): # read through every row in df

        # grab column data for the row
        lvl = col['teaching_level']
        exp = col['experience']
        skills = col['wanted_skills'].split(',')
        roles = str(col['role']).split(',')
        
        coded_level.append(level_code[lvl]) # pass through the school level they teach

        if exp in exp_code.keys(): # this if/else handles other/nan input
            coded_exp.append(exp_code[exp])
        else:
            coded_exp.append(exp)

        for j in range(len(skills)): # look at each skill selected
            s = skills[j].replace(' ', '')
            if s in skills_code.keys():
                skills[j] = s.replace(s, skills_code[s])
            else:
                skills[j] = '*' # for now mark free response with star
        coded_skills.append(skills)

        for j in range(len(roles)): # look at each role selected
            r = roles[j].replace(' ', '')
            if r in role_code.keys():
                roles[j] = r.replace(r, role_code[r])
            else:
                roles[j] = '*' # for now mark free response with star
        coded_roles.append(roles)
        
    return coded_exp, coded_skills, coded_roles, coded_level

def code_user_interests(user_interests):

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

################################
#         REC ALGORITHM        #
################################

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
    
def one_hot_encoding(user_model_df):
    one_hot_um = pd.DataFrame({})
    one_hot_um['experience'] = user_model_df['experience']
    one_hot_um['teaching_level'] = user_model_df['teaching_level']
    one_hot_um['teaching'] = [1 if 'teaching' in i else 0 for i in user_model_df['wanted_skills']]
    one_hot_um['coaching'] = [1 if 'coaching' in i else 0 for i in user_model_df['wanted_skills']]
    one_hot_um['leadership'] = [1 if 'leadership' in i else 0 for i in user_model_df['wanted_skills']]
    one_hot_um['digital'] = [1 if 'digital' in i else 0 for i in user_model_df['wanted_skills']]
    one_hot_um['multimedia'] = [1 if 'multimedia' in i else 0 for i in user_model_df['wanted_skills']]
    one_hot_um['*'] = [1 if '*' in i else 0 for i in user_model_df['wanted_skills']]
    one_hot_um['roles_T'] = [1 if 'T' in i else 0 for i in user_model_df['roles']]
    one_hot_um['roles_P'] = [1 if 'P' in i else 0 for i in user_model_df['roles']]
    one_hot_um['roles_O'] = [1 if 'O' in i else 0 for i in user_model_df['roles']]
    one_hot_um['roles_*'] = [1 if '*' in i else 0 for i in user_model_df['roles']]

    return one_hot_um

def produce_recommendations(user):
    user_lm = LearnerModel.objects.get(user=user)

    # Convert user model to fit rec sys preprocssing above 
    # TODO: tidy up!
    df = pd.DataFrame(columns=['teaching_level', 'experience', 'role', 'wanted_skills'])
    df.loc[0] = [user_lm.school_level, user_lm.years_of_experience, user_lm.role, user_lm.skill_interests]
    coded_exp1, coded_skills1, coded_roles1, coded_level1 = code_responses(df)
    user_model = pd.DataFrame({})
    user_model['experience'] = coded_exp1
    user_model['wanted_skills'] = coded_skills1
    user_model['roles'] = coded_roles1
    user_model['teaching_level'] = coded_level1
    one_hot_um = one_hot_encoding(user_model)

    # sample user data
    user_interests = one_hot_um.iloc[0][2:7] # these are input by users and can be changed at any time
    user_engagement = {'teaching':0.4, 'coaching':0.7, 'leadership':0.2, 'digital':0.6, 'multimedia':0.4} # TODO: we need to calculate this metric
    cluster_engagement = {'teaching':0.8, 'coaching':0.2, 'leadership':0.4, 'digital':0.95, 'multimedia':0.6} # TODO: we need to calculate this metric

    # TODO: this is just a failsafe if we haven't added a series completed dictionary yet
    if (not user_lm.series_completed): 
        user_lm.series_completed = json.dumps({'teaching': 1, 'coaching': 1, 'leadership':1})
        user_lm.save()

    # Get the databases tracks and iterate through them to find the following:
    max_track_num = {}  # dictionary {track: series count (max)}
    series_completed = json.loads(user_lm.series_completed) # dictionary {track: number of series that the user has completed}
    ranking = {'teaching': 0.84, 'coaching': 0.53, 'leadership':0.57, 'digital':0.81, 'multimedia':0.80}

    all_tracks = Track.objects.all()
    for t in all_tracks:
        max_track_num[t.title] = t.series_set.all().count()
    for key,value in max_track_num.items():
        if (key not in series_completed): 
            series_completed[key] = 0
    
    # Create final DataFrame for recommendations
    df = create_user_df(max_track_num, ranking, series_completed, user_interests, user_engagement, cluster_engagement)
    
    # create a new recommendation queue for this user
    recommended_tracks = recommend_videos(df)
    completed_modules = list(user.modulecompletion_set.all().values_list('module__video__id', flat=True))  # get list of all modules completed by the user
    rec_tracks = Track.objects.filter(title__in=recommended_tracks)  # get all relevant tracks for this user based on recs
    list_of_series_ids = []
    for t in rec_tracks:    
        for s in t.series_set.all():   
            curr_series_modules = list(s.video_set.all().values_list('id', flat=True)) # get list of all series
            check = all(item in completed_modules for item in curr_series_modules)
            if (not check): list_of_series_ids.append(s.id)

    recq,_ = RecommendationQueue.objects.get_or_create(user=user)
    recq.list_of_ids = list_of_series_ids
    recq.save()

################################
#           WEBPAGES           #
################################

def user_recs(request, user_id=0):

    if (user_id): curr_user = User.objects.get(pk=user_id)
    else: curr_user = request.user

    if (not RecommendationQueue.objects.filter(user=curr_user).exists()):
        produce_recommendations(curr_user)

    recommended_ids = json.loads(RecommendationQueue.objects.get(user=curr_user).list_of_ids)
    if len(recommended_ids) > 0:
        recommended_id = recommended_ids[0]
        # get list of completed modules and add to context (to filter out)
        completed_modules = list(curr_user.modulecompletion_set.all().values_list('module__id', flat=True))  
        completed_videos = list(curr_user.modulecompletion_set.all().values_list('module__video__id', flat=True))  
        curr_series = Series.objects.get(pk=recommended_id)
        curr_video = curr_series.video_set.order_by('series_order').exclude(id__in=completed_videos).first()
        curr_module = curr_video.module_set.first()

        # get secondary track
        series_in_curr_track = list(curr_series.track.series_set.all().values_list('id', flat=True))
        recommended_ids_2 = list(set(recommended_ids) - set(series_in_curr_track))
        if (len(recommended_ids_2)>0):
            recommended_id_2 = recommended_ids_2[0]
            curr_series_2 = Series.objects.get(pk=recommended_id_2)
            curr_video_2 = curr_series_2.video_set.order_by('series_order').exclude(id__in=completed_videos).first()
            curr_module_2 = curr_video_2.module_set.first()
            context = {"series": curr_series, "module": curr_module, "series2": curr_series_2, "module2": curr_module_2, "completed_modules": completed_modules}
        else:
            context = {"series": curr_series, "module": curr_module, "series2": None, "module2": None, "completed_modules": completed_modules}
    else:
        context = {"series": None, "module": None, "series2": None, "module2": None, "completed_modules": []}

    context['all_users'] = User.objects.all()
    return render(request, "recs.html", context=context)

def produce_feedback(user):
    feedback_thread = threading.Thread(target=core.Description, name="feedback_creator", args=(LearnerModel.objects.get(user=user),))
    feedback_thread.start()

def recommended_module(request, module_id):
    curr_module = Module.objects.get(pk=module_id)
    no_of_questions = curr_module.questions.count()

    if (no_of_questions==2): curr_form=Module2QForm
    elif (no_of_questions==3): curr_form=Module3QForm
    elif (no_of_questions==4): curr_form=Module4QForm
    else: curr_form=Module2QForm

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = curr_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # create new answer objects per answer
            for count, question in enumerate(curr_module.questions.all()):
                curr_answer = form.cleaned_data['answer{}'.format(count+1)]
                AnswerToVideoQuestion.objects.create(user=request.user, video=curr_module.video, question=question, answer=curr_answer)

            # TODO: add form input for feedback rating and feedback
            ModuleCompletion.objects.create(user = request.user, module = curr_module, time_spent = 30.0, complete = True, feedback_rating = 3.5, feedback='Good!')
            produce_recommendations(request.user)           # create new recommendation set for the user
            produce_feedback(request.user)     # create feedback for the user based on their new answers
            messages.info(request, "You completed: {}!".format(curr_module.title))
            return redirect("recsys:user_recs")
    else:
        form = curr_form()

    context = {"module": curr_module, "form": form}
    return render(request, "rec_module.html", context=context)

def expert_recs(request, user_id):
    # TODO: add easily swappable modules IF same video
    # TODO: add drag and drop interface for easily switching module order

    # Get the user in question
    if (user_id == 0): curr_user = User.objects.first()
    else: curr_user = User.objects.get(pk=user_id)

    if (not RecommendationQueue.objects.filter(user=curr_user).exists()):
        produce_recommendations(curr_user)

    # Get recommended modules, perserving the order of the recommendation list
    list_of_ids = json.loads(RecommendationQueue.objects.get(user=curr_user).list_of_ids)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_of_ids)])
    recommended_series = Series.objects.filter(id__in=list_of_ids).order_by(preserved)

    context = {"series": recommended_series, "curr_user": curr_user, "all_users": User.objects.all()}
    return render(request, "recs_expert.html", context=context)


def all_activities(request):
    curr_user = request.user
    all_tracks = Track.objects.all()
    completed_modules = list(curr_user.modulecompletion_set.all().values_list('module__id', flat=True))
    
    context = {"all_tracks": all_tracks, "completed_modules": completed_modules}
    return render(request, "all_activities.html", context=context)


################################
#          CLUSTERING          #
################################

def clustering(X, k, method='kmeans'):
    model = None
    if (method=='agglomerative'): model = AgglomerativeClustering(n_clusters=k).fit(X)
    elif (method=='spectral'): model = SpectralClustering(n_clusters=k, random_state=37).fit(X)
    else: model = KMeans(n_clusters=k, random_state=37).fit(X)
    labels = model.labels_
    return labels

def illustrate_cluster(labels, one_hot_df):
    clustered_groups = one_hot_df.copy()
    clustered_groups['cluster'] = labels
    
    cluster_means = clustered_groups.groupby('cluster').mean() # get cluster means
    cluster_counts = clustered_groups.groupby('cluster').count() # get cluster counts
    consider = cluster_means[['experience', 'teaching_level', 'roles_T']] # list of features we could highlight
    # we want to highlight the features for each cluster that are furthest from the mean
    highlight = consider.columns[np.argsort(np.array(abs((consider - np.mean(consider, axis=0))\
                                                         /np.mean(consider, axis=0))))[:, -2:]]
    cluster_msgs = {}
    for i in range(len(cluster_means)):
        msg = f"{cluster_counts.iloc[i]['experience']} people, "
        
        for h in highlight[i]:
            value = cluster_means.iloc[i][h]
            if 'roles_T' in h: msg = msg + f'{round(100*value)}% are teachers, '
            elif 'experience' in h: msg = msg + f'average experience is {round(value, 2)} years, '
            elif 'teaching_level' in h: msg = msg + f'Average school level is {round(value)}, '
            else: msg = msg + str(h) +  str(cluster_means.iloc[i][h])
        
        cluster_msgs[f'Cluster {i}'] = msg
    return cluster_msgs

def plotly_strip(df, labels, cluster_msgs, x='experience', y='teaching_level'):
    df = df.copy()
    df['cluster'] = labels
    df['cluster key'] = [cluster_msgs[f'Cluster {i}'] for i in df['cluster']]

    fig = px.strip(data_frame=df, x = "experience", y='teaching_level', color='cluster', 
               stripmode = "overlay", hover_data=['cluster key'])
    fig.update_traces({'marker':{'size': 20, 'line':{'width':1}, 'opacity':0.8}})
    plt_div = plot(fig, output_type='div')
    return plt_div

def user_clustering(request, method='kmeans', num_clusters=4, features='roles_T,teaching,experience'):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        new_features = request.POST.getlist('feature_select')

        if (len(new_features) == 0): new_features='roles_T,teaching,experience'
        else: new_features = ','.join(new_features)
        return redirect('recsys:user_clustering', method=request.POST['methodSelect'], num_clusters=int(request.POST['numSelect']), features=new_features)

    # df = pd.DataFrame(columns=['teaching_level', 'experience', 'role', 'wanted_skills'])
    df = pd.DataFrame(list(LearnerModel.objects.all().values('school_level', 'years_of_experience', 'role', 'skill_interests')))
    df = df.rename(columns={'school_level':'teaching_level', 'years_of_experience':'experience', 'skill_interests':'wanted_skills'})

    # Convert user model to fit rec sys preprocssing above 
    coded_exp1, coded_skills1, coded_roles1, coded_level1 = code_responses(df)
    user_model = pd.DataFrame({})
    user_model['experience'] = coded_exp1
    user_model['wanted_skills'] = coded_skills1
    user_model['roles'] = coded_roles1
    user_model['teaching_level'] = coded_level1
    one_hot_um = one_hot_encoding(user_model)

    split_features = features.split(',')
    X = np.array(one_hot_um[split_features])
    labels = clustering(X, num_clusters, method)
    cluster_msgs = illustrate_cluster(labels, one_hot_um)

    # Set the cluster for each learner in the DB
    clustered_df = pd.DataFrame(list(LearnerModel.objects.all().values()))
    clustered_df['labels'] = labels
    for index, row in clustered_df.iterrows():
        curr_learner = LearnerModel.objects.get(pk=row['id'])
        curr_learner.cluster = row['labels']
        curr_learner.save()

    context = {
        "learners": LearnerModel.objects.all(),
        "labels": labels,
        "cluster_msgs": cluster_msgs,
        "method": method,
        "num_clusters": num_clusters,
        "plot_div": plotly_strip(one_hot_um, labels, cluster_msgs, x='experience', y='teaching_level'),
        "features": split_features,
    }
    return render(request, "user_clustering.html", context=context)
