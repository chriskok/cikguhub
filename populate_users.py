from main.models import *
from django.contrib.auth.models import User
import pandas as pd
import re
import random
from django.db import IntegrityError

# ================================== #
#        UI FINAL EXAM - GRADED      #
# ================================== #

df = pd.read_csv('data/people.csv', header=0)

columns = ['Timestamp', 'E-mel / E-mail (E.g. cikguhub@myedvolution.com)',
       'Nombor Telefon / Phone Number (E.g. +60123456789)',
       'Nama Penuh / Full Name (As per NRIC)',
       '1. Anda mengajar di sekolah jenis? / Which school are you teaching in?',
       '2. Berapakah tahun anda menjadi pendidik? / How long have you been an educator?',
       '3. Apakah jawatan anda di sekolah? / What is your role in school?',
       '4. Apakah kemahiran yang anda ingin bangunkan? / What are the skills you wish to develop?',
       '5. Apakah bidang lain yang anda minat untuk pelajari? / What other areas you are interested to learn?',
]

exp_level_conversion = {
    'Kurang daripada 1 tahun / Less than 1 year': 0.5,
    '1 hingga 5 tahun / 1 to 5 years': 3.0,
    '6 hingga 10 tahun / 6 to 10 years': 8.0,
    'Lebih daripada 10 tahun / More than 10 years': 12.5,
}

for index, row in df.iterrows():
    email = row['E-mel / E-mail (E.g. cikguhub@myedvolution.com)']
    username = email.split('@')[0]
    password = "cikgupass"
    user, user_created = User.objects.get_or_create(username=username, email=email, password=password)
    if (user_created): print('User: {}-{} created'.format(username, index))
    years_of_experience = exp_level_conversion[row['2. Berapakah tahun anda menjadi pendidik? / How long have you been an educator?']]
    percentage_of_experience = years_of_experience/12.5*100
    planner_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20))),
    guardian_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20))),
    mentor_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20))),
    motivator_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20))),
    assessor_score = float(random.randint(max(0,int(percentage_of_experience)-20), min(100,int(percentage_of_experience)+20))),
    try:
        lm, created = LearnerModel.objects.get_or_create(user=user, 
            full_name = row['Nama Penuh / Full Name (As per NRIC)'],
            school_level = row['1. Anda mengajar di sekolah jenis? / Which school are you teaching in?'],
            years_of_experience = years_of_experience,
            role = row['3. Apakah jawatan anda di sekolah? / What is your role in school?'],
            skill_interests = row['4. Apakah kemahiran yang anda ingin bangunkan? / What are the skills you wish to develop?'],
            other_interests = row['5. Apakah bidang lain yang anda minat untuk pelajari? / What other areas you are interested to learn?'],
            planner_score = planner_score[0],
            guardian_score = guardian_score[0],
            mentor_score = mentor_score[0],
            motivator_score = motivator_score[0],
            assessor_score = assessor_score[0],
            current_feedback = Feedback.objects.create(user=user, feedback="",
                planner_score = planner_score[0],
                guardian_score = guardian_score[0],
                mentor_score = mentor_score[0],
                motivator_score = motivator_score[0],
                assessor_score = assessor_score[0],
            )
        )
        # TODO: create recommendation queue object with recsys function
        if (created): print('LearnerModel: {}-{} created'.format(lm.full_name, index))
    except IntegrityError as e: 
        if 'unique constraint' in e.args:
            print(e)
            print('Failed with: {}'.format(username))
            continue 

