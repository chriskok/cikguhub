import openai
import json
from report import core
from main.models import *

try:
    with open('api_keys.json', 'r') as f:
        import openai
        api_keys = json.load(f)
        openai.api_key = api_keys['openai']
        openai_enabled = True
except:
    openai_api_key = None
    message = "No OpenAI API key found. Please add one to api_keys.json."

def generate_response(vid_title, vid_desc, question, metric, target_score):
    result = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages = [{"role": "system", "content" : 
    f"""You are an expert teacher trainer writing feedback for teachers learning how to be {', '.join([f'{m}, meaning {d}' for m, d in core.metrics.items()])}. You are going to be given a question and will be asked to generate a response that might score a certain score on a certain competency."""},
    {"role": "user", "content" : 
    f"""Write a response to this question that might score 50 / 100 on the Mentor competency.
    
    Here is the question: How would you apply the knowledge you learned from this video to your own teaching?"""},
    {"role": "assistant", "content" : 
    """Honestly, I don't really know because I wasn't paying a lot of attention, but I'd probably give students candy if they behaved or something?"""},
    {"role": "user", "content" : 
    f"""Write a response to this question that might score {target_score} / 100 on the {metric} competency.
    
    Here is the question: {question}"""}
    ])
    return result.choices[0].message.content

def generate_response_2(vid_title, vid_desc, question, metrics):
    scores_and_desc = ', '.join([f'{metrics[m]}/100 for {d.name}, meaning {d.description}' for m, d in core.metrics.items()])

    result = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages = [{"role": "system", "content" : 
    f"""You are an example answer generator. You are going to be given a question and will be asked to generate a response that will reflect your scores on certain competencies. Even if you don't have enough information, just make it up."""},
    {"role": "user", "content" : 
    f"""Write a 2 sentence response to the question "How would you apply the knowledge you learned from this video to your own teaching?" to the video: Using Candy As A Reward (video description: This is a video about how a teacher might utilize candy as a positive motivation method in their lesson plans), that would reflect your scores on the following competencies: Listening Skills: 10/100, Motivational Ideation: 60/100"""},
    {"role": "assistant", "content" : 
    """Honestly, I don't really know because I wasn't paying a lot of attention, but I'd probably give students candy if they behaved or something?"""},
    {"role": "user", "content" : 
    f"""Write a 2 sentence response to the question {question} to the video: {vid_title} (video description: {vid_desc}) that would reflect your scores on the following competencies: {scores_and_desc}"""}
    ])

    return result.choices[0].message.content

def populate_all_responses():
    # get users
    user_models = LearnerModel.objects.all()
    # get videos
    modules = Module.objects.all()
    for module in modules[6:20]:  # TODO: expand range to add more modules 
        if (module.title.endswith("_advanced")): continue
        video_title = module.video.title
        video_desc = module.video.description
        video_questions = module.video.videoquestion_set.all()
        for user_model in user_models[:10]:  # TODO: expand range to add more users who respond 
            metrics = {}
            metrics['planner'] = user_model.planner_score
            metrics['guardian'] = user_model.guardian_score
            metrics['mentor'] = user_model.mentor_score
            metrics['motivator'] = user_model.motivator_score
            metrics['assessor'] = user_model.assessor_score
            print("Video Title: {}\nVideo Desc: {}\nUser: {}\nMetrics: {}".format(video_title, video_desc, user_model.full_name, metrics))
            # create answer for each question
            for q in video_questions:
                answer = generate_response_2(video_title, video_desc, q.question, metrics)
                print("Question: {}, Answer: {}".format(q.question, answer))
                AnswerToVideoQuestion.objects.create(user=user_model.user, video=module.video, question=q, answer=answer)
        # create module compleition object once all questions are answered
        ModuleCompletion.objects.create(user=user_model.user, module=module, time_spent=30.0, complete=True)

populate_all_responses()
