import json
from main.models import *
from .relevant import get_relevant_answers
metric_descriptions = {
    "planner": "Teachers act as planners to ensure readiness and thorough preparation in implementing Learning and Facilitation.",
    "guardian": "Teachers act as controllers of class objective implementation to ensure the smoothness of the learning process according to plan.",
    "mentor": "Teachers act as guides to enable students to master knowledge, skills and practice values based on lesson objectives.",
    "motivator": "Teachers act as motivators to increase students' motivation and soft skills.",
}

openai_enabled = False

try:
    with open('api_keys.json', 'r') as f:
        import openai
        api_keys = json.load(f)
        openai.api_key = api_keys['openai']
        openai_enabled = True

except:
    openai_api_key = None
    message = "No OpenAI API key found. Please add one to api_keys.json."

class Description:
    def __init__(self, learner_model):
        self.learner_model = learner_model
        self.description = self.generate()

    def generate(self):
        if not openai_enabled:
            return f"""NO API KEY FOUND -- USING FALLTHROUGH METHOD {self.learner_model.full_name} has the following ratings:   
Planner: {self.learner_model.planner_score}
Guardian: {self.learner_model.guardian_score}
Mentor: {self.learner_model.mentor_score}
Motivator: {self.learner_model.motivator_score}
Assesssor: {self.learner_model.assessor_score}
{message}
"""


        responses = AnswerToVideoQuestion.objects.filter(user=self.learner_model.user).all()

        relevant_responses = get_relevant_answers(self.learner_model)

        user_prompt = f"""
Teacher {self.learner_model.user} has scores {', '.join([f'{m}: {int(getattr(self.learner_model, m + "_score"))}.' for m in metric_descriptions])}.
Here are some of their recent replies to questions on videos: {relevant_responses}
"""

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages = [{"role": "system", "content" : 
f"""You are an expert teacher trainer writing feedback for teachers learning how to be {', '.join([f'{m}, meaning {d}' for m, d in metric_descriptions.items()])}. You are given a learner's name and their scores out of 100 on each of the five competencies. You are asked to write a description of the learner that highlights their strengths and weaknesses, mentioning specific responses that they gave on assignments."""},
            {"role": "user", "content" : 
"""Teacher Christopher Kok has scores Planner: 20, Guardian: 60, Mentor: 70, Motivator: 5, Assessor: 90. He recently wrote on a Planning assignment that 'I don't think planning really matters, I just like to wing it', on a Guardian assignment that 'I believe in encouraging positive student leadership and taking a back seat on guardianship', on a Mentor assignment that 'I thoroughly evaluate students and give them quality feedback', on a Motivator assignment that 'I don't think motivation is really important, in fact I try to make my students upset as often as possible.', and on an Assessor assignment that 'I believe in giving students a lot of feedback and letting them self-assess'."""},
            {"role": "assistant", "content" : 
"""As a teacher, you have strengths in some areas and need to improve in others. Your scores in the competencies of Planner, Guardian, Mentor, Motivator, and Assessor indicate that you are strong in assessing students and providing quality feedback. However, you scored low in planning and motivating students.

Your score of 90 in the Assessor competency shows that <b>you are dedicated to helping your students improve by providing them with feedback and encouraging self-assessment.</b> You scored 60 in Guardian and 70 in Mentor, demonstrating your <b>commitment to empowering your students to take responsibility for their own learning and helping them master knowledge and skills</b>.

However, your scores of 20 in Planner and 5 in Motivator indicate that <b>you need to work on your planning and motivational skills</b>. Your response to the Planning assignment suggests that <b>you don't think planning really matters and prefer to wing it, which is a concerning attitude for a teacher</b>. In your Motivator assignment, you stated that <b>you don't think motivation is important and even try to make your students upset, which is a major weakness as motivating students is a key aspect of teaching.</b>"""},
            {"role": "user", "content" : user_prompt}]
        )
        return result.choices[0].message.content + f"<br><br><br>DEBUG: {relevant_responses}"

    def __str__(self):
        return str(self.description)