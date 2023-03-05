from django.contrib import admin
from .models import *

admin.site.register(LearnerModel)
admin.site.register(Video)
admin.site.register(VideoQuestion)
admin.site.register(VideoCompletion)
admin.site.register(AnswerToVideoQuestion)