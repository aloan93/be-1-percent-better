from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20, null=False)

    def __str__(self):
        return self.username

class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    external_exercise_id = models.IntegerField(null=False)
    external_exercise_name = models.CharField(max_length=100, null=False)
    personal_best = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.user_id) + " " + self.external_exercise_name
    
class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    session_name = models.CharField(max_length=30, null=False)
    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=False)
    date_time = models.DateTimeField(auto_now_add=True)
    reps = models.PositiveSmallIntegerField(null=False)
    weight_kg = models.PositiveSmallIntegerField(null=False)
    sets = models.PositiveSmallIntegerField(null=False)

    def __str__(self):
        return str(self.session_id) + " " + self.session_name



    
