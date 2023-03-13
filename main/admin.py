from django.contrib import admin
from .models import *

admin.site.register(Feedback)
admin.site.register(LearnerModel)
admin.site.register(Video)
admin.site.register(VideoQuestion)
admin.site.register(Module)
admin.site.register(ModuleCompletion)
admin.site.register(Track)
admin.site.register(Series)
admin.site.register(AnswerToVideoQuestion)
admin.site.register(RecommendationQueue)