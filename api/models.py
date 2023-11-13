from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class ExtendUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(blank=False, max_length=255, verbose_name='email')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username

class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    external_exercise_id = models.CharField(max_length=4, null=False)
    external_exercise_name = models.CharField(max_length=100, null=False)
    external_exercise_bodypart = models.CharField(max_length=20, null=False)
    personal_best = models.SmallIntegerField(default=0)

    def __str__(self):
        return 'User: ' + str(self.user_id) + ", Exercise: " + self.external_exercise_name
    
class WorkoutLog(models.Model):
    workout_id = models.AutoField(primary_key=True)
    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=False)
    date_time = models.DateTimeField(auto_now_add=True)
    reps = models.PositiveSmallIntegerField(null=False)
    weight_kg = models.PositiveSmallIntegerField(null=False)
    sets = models.PositiveSmallIntegerField(null=False)

    def __str__(self):
        return 'Workout ID: ' + str(self.workout_id) + ", Exercise ID: " + str(self.exercise_id)
    
class SessionLog(models.Model):
    session_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    date_time = models.DateTimeField(auto_now_add=True)
    session_name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return 'User: ' + str(self.user_id) + ', Session: ' + self.session_name


class SessionLog_Exercise(models.Model):
    session_exercise_id = models.AutoField(primary_key=True)
    session_id = models.ForeignKey(SessionLog, on_delete=models.CASCADE, null=False)
    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return 'Session ID: ' + str(self.session_id) + ', Exercise ID: ' + str(self.exercise_id) 