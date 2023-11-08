import graphene
from graphene_django import DjangoObjectType 
from .models import User, Exercise, WorkoutLog, SessionLog, SessionLog_Exercise

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise
        fields = '__all__'

class SessionLogType(DjangoObjectType):
    class Meta:
        model = SessionLog
        fields = '__all__'

class WorkoutLogType(DjangoObjectType):
    class Meta:
        model = WorkoutLog
        fields = '__all__'

class SessionLog_ExerciseType(DjangoObjectType):
    class Meta:
        model = SessionLog_Exercise
        fields = '__all__'


class Query(graphene.ObjectType):

    get_all_users = graphene.List(UserType)
    get_user_by_user_id = graphene.Field(UserType, user_id=graphene.Int())
    
    get_all_exercises = graphene.List(ExerciseType)
    get_exercises_by_user_id = graphene.List(ExerciseType, user_id=graphene.Int())
    get_exercise_by_exercise_id = graphene.Field(ExerciseType, exercise_id=graphene.Int())

    get_all_sessions = graphene.List(SessionLogType)
    get_sessions_by_user_id = graphene.List(SessionLogType, user_id=graphene.Int())
    get_session_by_session_id = graphene.Field(SessionLogType, session_id=graphene.Int())

    get_all_workouts = graphene.List(WorkoutLogType)
    get_workouts_by_exercise_id = graphene.List(WorkoutLogType, exercise_id=graphene.Int())
    get_workout_by_workout_id = graphene.Field(WorkoutLogType, workout_id=graphene.Int())

    get_exercises_by_session_id = graphene.List(SessionLog_ExerciseType, session_id=graphene.Int())

    def resolve_get_all_users(self, info):
        return User.objects.all()
    
    def resolve_get_user_by_user_id(self, info, user_id):
        return User.objects.get(pk=user_id)
    
    def resolve_get_all_exercises(self, info):
        return Exercise.objects.all()
    
    def resolve_get_exercises_by_user_id(self, info, user_id):
        return Exercise.objects.filter(user_id=user_id)
    
    def resolve_get_exercise_by_exercise_id(self, info, exercise_id):
        return Exercise.objects.get(pk=exercise_id)
    
    def resolve_get_all_sessions(self, info):
        return SessionLog.objects.all()
    
    def resolve_get_sessions_by_user_id(self, info, user_id):
        return SessionLog.objects.filter(user_id=user_id)
    
    def resolve_get_session_by_session_id(self, info, session_id):
        return SessionLog.objects.get(pk=session_id)
    
    def resolve_get_all_workouts(self, info):
        return WorkoutLog.objects.all()
    
    def resolve_get_workouts_by_exercise_id(self, info, exercise_id):
        return WorkoutLog.objects.filter(exercise_id=exercise_id)
    
    def resolve_get_workout_by_workout_id(self, info, workout_id):
        return WorkoutLog.objects.get(pk=workout_id)
    
    def resolve_get_exercises_by_session_id(self, info, session_id):
        return SessionLog_Exercise.objects.filter(session_id=session_id)
    
class UserMutationCreate(graphene.Mutation):

    class Arguments:
        username= graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, username):
        user = User(username=username)
        user.save()
        return UserMutationCreate(user = user)

class UserMutationUpdate(graphene.Mutation):

    class Arguments:
        user_id = graphene.ID(required = True)
        username = graphene.String(required = True)
    
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, user_id, username):
        user = User.objects.get(user_id = user_id)
        user.username = username
        user.save()
        return UserMutationUpdate(user = user)


class UserMutationDelete(graphene.Mutation):

    class Arguments:
        user_id = graphene.ID(required = True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, user_id):
        user = User.objects.get(user_id = user_id)
        user.delete()
        return

class Mutation(graphene.ObjectType):

    create_user = UserMutationCreate.Field()
    update_user = UserMutationUpdate.Field()
    delete_user = UserMutationDelete.Field() 

schema = graphene.Schema(query=Query, mutation=Mutation)