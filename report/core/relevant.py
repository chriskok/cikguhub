from main.models import *
from utils import generate_embedding
from .defined_metrics import defined_metrics

def get_relevant_answers(usermodel, n=3):
    # get all answers 
    completed_modules = ModuleCompletion.objects.filter(user=usermodel.user).all()
    all_answers = []

    for module in completed_modules:
        all_answers_for_module = AnswerToVideoQuestion.objects.filter(user=usermodel.user, question__in=module.module.questions.all())

        all_answers.extend(list(all_answers_for_module))

    # find the most relevant answers for each metric
    metrics = {
        "planner": (usermodel.planner_score, defined_metrics["planner"]),
        "guardian": (usermodel.guardian_score, defined_metrics["guardian"]),
        "mentor": (usermodel.mentor_score, defined_metrics["mentor"]),
        "motivator": (usermodel.motivator_score, defined_metrics["motivator"]),
        "assessor": (usermodel.assessor_score, defined_metrics["assessor"]),
    }

    # get embeddings for all answers (top 100 for now)
    embeddings = {
        a: generate_embedding(a.answer) for a in all_answers[:100]
    }

    # get top n answers for each metric
    sel = []
    for metric in metrics.items():
        m = metric[1][1]

        # get relevance of each answer to this metric
        relevance = {
            a: m.relevance(embeddings[a]) for a in all_answers
        }

        # get top 5 answers for this metric
        top_answers = sorted(relevance.items(), key=lambda x: x[1], reverse=True)[:n]

        # add to sel
        sel += [(x[0].question.question, x[0].answer, metric[0]) for x in top_answers]

    return sel #[f"question: {x[0]}, answer: {x[1]}, emphasis: {x[2]}" for x in sel]