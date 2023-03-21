from main.models import *

def get_relevant_answers(usermodel):
    # get all answers 
    completed_modules = ModuleCompletion.objects.filter(user=usermodel.user).all()
    all_answers = []

    for module in completed_modules:
        all_questions_for_module = module.module.questions.all()
        all_answers_for_module = AnswerToVideoQuestion.objects.filter(user=usermodel.user, question__in=module.module.questions.all())
        # print(all_answers_for_module)
        all_answers.extend(list(all_answers_for_module))
        # TODO: embed answers and find most relevant ones

    return [f"question: {x.question}, answer: {x.answer}" for x in all_answers[:5]]