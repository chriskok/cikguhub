from django.db import models
from django.contrib.auth.models import User

class LearnerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1024, null=True, blank=True)
    years_of_experience = models.FloatField(default=0.0)
    role = models.CharField(max_length=4096, null=True, blank=True)
    skill_interests = models.TextField(max_length=4096, null=True, blank=True)
    other_interests = models.TextField(max_length=4096, null=True, blank=True)

    planner_score = models.FloatField(default=0.0)
    guardian_score = models.FloatField(default=0.0)
    mentor_score = models.FloatField(default=0.0)
    motivator_score = models.FloatField(default=0.0)
    assessor_score = models.FloatField(default=0.0)

    feedback = models.TextField(max_length=4096, null=True, blank=True)
    human_approved = models.BooleanField(default=False)
    human_edited = models.BooleanField(default=False)
    feedback_edit_history = models.TextField(null=True, blank=True)

class Video(models.Model):
    title = models.CharField(max_length=4096)
    tags = models.CharField(max_length=4096, help_text = "comma-separated list of tags")
    url = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return "{}".format(self.title)

class VideoQuestion(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    question = models.CharField(max_length=4096)
    type = models.CharField(max_length=100)   # MCQ (multiple choice) or OEQ (open-ended)
    possible_answers = models.CharField(max_length=4096, null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.video, self.question)

class VideoCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watchtime = models.FloatField(null=True, blank=True, default=0.0)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return "{} finished {}".format(self.user, self.video)

class AnswerToVideoQuestion(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    question = models.ForeignKey(VideoQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=4096)

    def __str__(self):
        return "{}: {} - {}".format(self.video, self.question, str(self.id))

class RecommendationQueue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    list_of_video_ids = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return "{}: {} ".format(self.user, self.list_of_video_ids)
