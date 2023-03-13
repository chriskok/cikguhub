from main.models import *
from django.contrib.auth.models import User
from django.db import IntegrityError

import pandas as pd
import re
import random

# ================================== #
#           POPULATE VIDEOS          #
# ================================== #

questions=["What did you learn from this video?", "How have you applied these lessons in your classroom in the past?", "Based on your experience, what would you add to this video?"]
exp_levels= ['beginner', 'advanced']

df = pd.read_csv('data/video_data.csv', header=0)

for index, row in df.iterrows():
    series = row['series']
    title = row['title']
    description = row['description']
    embed_url = row['embed_url']
    level = row['level']
    track = row['track']
    primary = row['primary']
    secondary = row['secondary']
    admin = row['admin']
    # CREATE TRACK
    track, track_created = Track.objects.get_or_create(title=track)
    if (track_created): print('Track: {}-{} created'.format(track, index))
    # CREATE SERIES
    series, series_created = Series.objects.get_or_create(title=series, track=track, track_order=level, 
                                                          primary_level=True if primary==1 else False,
                                                          secondary_level=True if secondary==1 else False,
                                                          admin_level=True if admin==1 else False,
                                                          )
    if (series_created): print('Series: {}-{} created'.format(series, index))
    video_tags = ""
    if (primary==1): video_tags+="primary,"
    if (secondary==1): video_tags+="secondary,"
    if (admin==1): video_tags+="admin,"
    existing_videos_count = series.video_set.count()
    try:
        # CREATE VIDEO
        video, video_created = Video.objects.get_or_create(title=title, tags=video_tags, description=description, 
                                                        url=embed_url, series=series)
        if (video_created): 
            print('Video: {}-{} created'.format(title, index))
            video.series_order=existing_videos_count+1
            video.save()
        # CREATE QUESTIONS FOR EACH VIDEO AND ASSOCIATED MODULES
        for video_question in questions:
            v_q, question_created = VideoQuestion.objects.get_or_create(video=video, question=video_question, type="OEQ")
            if (question_created): print('Question: {}: {}-{} created'.format(video.title, video_question, index))
            # ADD QUESTION TO BEGINNER MODULE
            b_module, b_module_created = Module.objects.get_or_create(video=video, title=video.title+"_beginner")
            if (video_question != "Based on your experience, what would you add to this video?"): b_module.questions.add(v_q)
            # ADD QUESTION TO ADVANCED MODULE
            a_module, a_module_created = Module.objects.get_or_create(video=video, title=video.title+"_advanced")
            a_module.questions.add(v_q)
    except IntegrityError as e: 
        if 'UNIQUE constraint' in e.args:
            print(e)
            print('Failed with: {}, url: {}'.format(title, embed_url))
            continue 

# class Module(models.Model):
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     questions = models.ManyToManyField(VideoQuestion)
#     title = models.CharField(max_length=4096, null=True, blank=True)

#     def __str__(self):
#         module_name = self.title if self.title else str(self.id)
#         return "{}. {}".format(str(self.id), module_name)


