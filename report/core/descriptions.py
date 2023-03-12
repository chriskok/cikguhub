class Description:
    def __init__(self, learner_model):
        self.learner_model = learner_model
        self.description = ">:("
        self.generate()

    def generate(self):
        self.description = f"""{self.learner_model.full_name} has the following ratings:
        
        Planner: {self.learner_model.planner_score}
        Guardian: {self.learner_model.guardian_score}
        Mentor: {self.learner_model.mentor_score}
        Motivator: {self.learner_model.motivator_score}
        Assesssor: {self.learner_model.assessor_score}
        """

    def __str__(self):
        return str(self.description)
