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

class ExerciseMutationCreate(graphene.Mutation):

    class Arguments:
        user_id = graphene.ID(required=True)
        external_exercise_id = graphene.String(required=True)
        external_exercise_name = graphene.String(required=True)
        external_exercise_bodypart = graphene.String(required=True)

    exercise = graphene.Field(ExerciseType)

    @classmethod
    def mutate(cls, root, info, user_id, external_exercise_id, external_exercise_name, external_exercise_bodypart):
        user_obj = User.objects.get(user_id=user_id)
        exercise = Exercise(user_id=user_obj, external_exercise_id=external_exercise_id, external_exercise_name=external_exercise_name, external_exercise_bodypart=external_exercise_bodypart)
        exercise.save()
        return ExerciseMutationCreate(exercise=exercise)
    
class ExerciseMutationUpdate(graphene.Mutation):

    class Arguments:
        exercise_id = graphene.ID(required=True)
        personal_best = graphene.Int(required=True)

    exercise = graphene.Field(ExerciseType)

    @classmethod
    def mutate(cls, root, info, exercise_id, personal_best):
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        exercise.personal_best = personal_best
        exercise.save()
        return ExerciseMutationUpdate(exercise=exercise)

class ExerciseMutationDelete(graphene.Mutation):

    class Arguments:
        exercise_id = graphene.ID(required=True)

    exercise = graphene.Field(ExerciseType)

    @classmethod
    def mutate(cls, root, info, exercise_id):
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        exercise.delete()
        return

class WorkoutMutationCreate(graphene.Mutation):

    class Arguments:
        exercise_id = graphene.ID(required=True)
        weight_kg = graphene.Int(required=True)
        reps = graphene.Int(required=True)
        sets = graphene.Int(required=True)

    workout = graphene.Field(WorkoutLogType)

    @classmethod
    def mutate(cls, root, info, exercise_id, weight_kg, reps, sets):
        exercise_obj = Exercise.objects.get(exercise_id=exercise_id)
        workout = WorkoutLog(exercise_id=exercise_obj, weight_kg=weight_kg, reps=reps, sets=sets)
        workout.save()
        return WorkoutMutationCreate(workout=workout)

class WorkoutMutationUpdate(graphene.Mutation):

    class Arguments:
        workout_id = graphene.ID(required=True)
        weight_kg = graphene.Int(required=True)
        reps = graphene.Int(required=True)
        sets = graphene.Int(required=True)

    workout = graphene.Field(WorkoutLogType)

    @classmethod
    def mutate(cls, root, info, workout_id, weight_kg, reps, sets):
        workout = WorkoutLog.objects.get(workout_id=workout_id)
        workout.weight_kg = weight_kg
        workout.reps = reps
        workout.sets = sets
        workout.save()
        return WorkoutMutationUpdate(workout=workout)

class WorkoutMutationDelete(graphene.Mutation):

    class Arguments:
        workout_id = graphene.ID()

    workout = graphene.Field(WorkoutLogType)

    @classmethod
    def mutate(cls, root, info, workout_id):
        workout = WorkoutLog.objects.get(workout_id=workout_id)
        workout.delete()
        return

class SessionMutationCreate(graphene.Mutation):

    class Arguments:
        user_id = graphene.ID()
        session_name = graphene.String()

    session = graphene.Field(SessionLogType)

    @classmethod
    def mutate(cls, root, info, user_id, session_name):
        user_obj = User.objects.get(user_id=user_id)
        session = SessionLog(user_id=user_obj, session_name=session_name)
        session.save()
        return SessionMutationCreate(session=session)
    
class SessionMutationUpdate(graphene.Mutation):

    class Arguments:
        session_id = graphene.ID()
        session_name = graphene.String()

    session = graphene.Field(SessionLogType)

    @classmethod
    def mutate(cls, root, info, session_id, session_name):
        session = SessionLog.objects.get(session_id=session_id)
        session.session_name = session_name
        session.save()
        return SessionMutationUpdate(session=session)


class Mutation(graphene.ObjectType):

    create_user = UserMutationCreate.Field()
    update_user = UserMutationUpdate.Field()
    delete_user = UserMutationDelete.Field()

    create_exercise = ExerciseMutationCreate.Field()
    update_exercise = ExerciseMutationUpdate.Field()
    delete_exercise = ExerciseMutationDelete.Field()

    create_workout = WorkoutMutationCreate.Field()
    update_workout = WorkoutMutationUpdate.Field()
    delete_workout = WorkoutMutationDelete.Field()

    create_session = SessionMutationCreate.Field()
    update_session = SessionMutationUpdate.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)