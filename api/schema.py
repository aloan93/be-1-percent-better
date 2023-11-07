import graphene
from graphene_django import DjangoObjectType 
from .models import User, Exercise, WorkoutLog, SessionLog, SessionLog_Exercise

class UserType(DjangoObjectType):
    class Meta:
        model = User

class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise

class Query(graphene.ObjectType):

    get_all_users = graphene.List(UserType)
    get_user_by_user_id = graphene.Field(UserType, user_id=graphene.Int())
    
    get_all_exercises = graphene.List(ExerciseType)
    get_exercises_by_user_id = graphene.List(ExerciseType, user_id=graphene.Int())


    def resolve_get_all_users(self, info):
        return User.objects.all()
    
    def resolve_get_user_by_user_id(self, info, user_id):
        return User.objects.get(pk=user_id)
    
    def resolve_get_all_exercises(self, infor):
        return Exercise.objects.all()
    
    def resolve_get_exercises_by_user_id(self, info, user_id):
        return Exercise.objects.filter(user_id=user_id)

schema = graphene.Schema(query=Query)