from django.contrib import admin
from .models import ExtendUser, Exercise, SessionLog, WorkoutLog, SessionLog_Exercise

admin.site.register(ExtendUser)
admin.site.register(Exercise)
admin.site.register(SessionLog)
admin.site.register(SessionLog_Exercise)
admin.site.register(WorkoutLog)



