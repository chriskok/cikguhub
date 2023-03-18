import openai
from report import core

def generate_response(question, metric, target_score):
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