from graphene.test import Client
from api.schema import schema
from api.models import User, Exercise, WorkoutLog
import pytest

@pytest.mark.django_db
def test_get_all_users():
    # Create test users in the database
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    # Make the GraphQL query
    query = '''
        query {
            getAllUsers {
                userId
                username
            }
        }
    '''
    
    # Initialise this client with the schema 
    client = Client(schema)
    # execute() method of the client is then called with the query, which sends the query to the GraphQL API.
    executed = client.execute(query)
    
    # Check the response is correct 
    assert executed == {
        'data': {
            'getAllUsers': [
                {'userId': str(user1.user_id), 'username': user1.username},
                {'userId': str(user2.user_id), 'username': user2.username}
            ]
        }
    }

@pytest.mark.django_db
def test_get_all_exercises():
    user = User.objects.create(username='testuser')

    exercise1 = Exercise.objects.create(user_id=user, external_exercise_id='1234', external_exercise_name='Squat', external_exercise_bodypart='Lower Legs', personal_best=0)
    exercise2 = Exercise.objects.create(user_id=user, external_exercise_id='5678', external_exercise_name='Bicep curl', external_exercise_bodypart='Upper Arms', personal_best=0)

    query = '''
        query {
            getAllExercises {
                exerciseId
                externalExerciseId
                externalExerciseName
                externalExerciseBodypart
                personalBest
                userId {
                    userId
                    username
                }
            }
        }
    '''
    client = Client(schema)
    executed = client.execute(query)
    assert executed == {
        'data': {
            'getAllExercises': [
                {
                    'exerciseId': str(exercise1.exercise_id),
                    'externalExerciseId': exercise1.external_exercise_id,
                    'externalExerciseName': exercise1.external_exercise_name,
                    'externalExerciseBodypart': exercise1.external_exercise_bodypart,
                    'personalBest': exercise1.personal_best,
                    'userId': {'userId': str(user.user_id), 'username': user.username}
                },
                {
                    'exerciseId': str(exercise2.exercise_id),
                    'externalExerciseId': exercise2.external_exercise_id,
                    'externalExerciseName': exercise2.external_exercise_name,
                    'externalExerciseBodypart': exercise2.external_exercise_bodypart,
                    'personalBest': exercise2.personal_best,
                    'userId': {'userId': str(user.user_id), 'username': user.username}
                }
            ]
        }
    }


@pytest.mark.django_db
def test_get_all_exercises_is_empty():

    query = '''
        query {
            getAllExercises {
                exerciseId
                externalExerciseId
                externalExerciseName
                externalExerciseBodypart
                personalBest
                userId {
                    userId
                    username
                }
            }
        }
    '''
    client = Client(schema)
    executed = client.execute(query)
    assert executed == {
        'data': {
            'getAllExercises': []
        }
    }

@pytest.mark.django_db
def test_get_users_by_user_id():
    
    testuser1 = User.objects.create(username='testuser1')
    testuser2 = User.objects.create(username='testuser2')
    
   
    query = '''
       query {
                getUserByUserId(userId: 6) {
                    userId
                    username
            }
        }
    '''
    
    client = Client(schema)
    
    executed = client.execute(query)
    
  
    assert executed == {
        'data': {
            'getUserByUserId': 
                {'userId': str(testuser2.user_id), 'username': testuser2.username}
        }
    }

@pytest.mark.django_db
def test_get_users_by_nonexisting_user_id():
    
   
    query = '''
       query {
                getUserByUserId(userId: 344) {
                    userId
                    username
            }
        }
    '''
    
    client = Client(schema)
    
    executed = client.execute(query)
    
  
    assert executed == {
        'data': {
            'getUserByUserId': 
                None
        },
        'errors': [{
            'locations': [{
                        'column': 17,
                        'line': 3}],
            'message': 'User matching query does not exist.',
            'path': ['getUserByUserId']}],
            
    }

@pytest.mark.django_db
def test_get_users_by_invalid_string_user_id():
    
   
    query = '''
       query {
                getUserByUserId(userId: 'banana') {
                    userId
                    username
            }
        }
    '''
    
    client = Client(schema)
    
    executed = client.execute(query)
    
  
    assert executed['data'] == None
    assert executed['errors']


@pytest.mark.django_db
def test_get_exercise_by_exercise_id():

    testuserjim = User.objects.create(username='jimsgains')
    testexercise = Exercise.objects.create(user_id=testuserjim, external_exercise_id='1004', external_exercise_name='Leg Press', external_exercise_bodypart='Lower Legs', personal_best=0)
   
    query = '''
       query {
            getExerciseByExerciseId(exerciseId: 3) {
                exerciseId
                externalExerciseId
                externalExerciseName
                externalExerciseBodypart
                personalBest
                userId {
                    userId
                    username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed == {
        'data': {
            'getExerciseByExerciseId': {
                    'exerciseId': str(testexercise.exercise_id),
                    'externalExerciseId': testexercise.external_exercise_id,
                    'externalExerciseName': testexercise.external_exercise_name,
                    'externalExerciseBodypart': testexercise.external_exercise_bodypart,
                    'personalBest': testexercise.personal_best,
                    'userId': {'userId': str(testuserjim.user_id), 'username': testuserjim.username}
            }
                
        }
    }

@pytest.mark.django_db
def test_get_exercises_by_user_id():

    testuserjill = User.objects.create(username='jillsgains')

    testexercise = Exercise.objects.create(user_id=testuserjill, external_exercise_id='1004', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=10)
    testexercise2 = Exercise.objects.create(user_id=testuserjill, external_exercise_id='1024', external_exercise_name='Sumo Squat', external_exercise_bodypart='Upper Legs', personal_best=10)
    testexercise3 = Exercise.objects.create(user_id=testuserjill, external_exercise_id='1324', external_exercise_name='Romanian Deadlift', external_exercise_bodypart='Upper Legs', personal_best=20)

    query = '''
       query {
            getExercisesByUserId(userId: 8) {
                exerciseId
                externalExerciseId
                externalExerciseName
                externalExerciseBodypart
                personalBest
                userId {
                    userId
                    username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed == {
        'data': {
            'getExercisesByUserId': [{
                    'exerciseId': str(testexercise.exercise_id),
                    'externalExerciseId': testexercise.external_exercise_id,
                    'externalExerciseName': testexercise.external_exercise_name,
                    'externalExerciseBodypart': testexercise.external_exercise_bodypart,
                    'personalBest': testexercise.personal_best,
                    'userId': {'userId': str(testuserjill.user_id), 'username': testuserjill.username}
            },{
                    'exerciseId': str(testexercise2.exercise_id),
                    'externalExerciseId': testexercise2.external_exercise_id,
                    'externalExerciseName': testexercise2.external_exercise_name,
                    'externalExerciseBodypart': testexercise2.external_exercise_bodypart,
                    'personalBest': testexercise2.personal_best,
                    'userId': {'userId': str(testuserjill.user_id), 'username': testuserjill.username}
            },{
                    'exerciseId': str(testexercise3.exercise_id),
                    'externalExerciseId': testexercise3.external_exercise_id,
                    'externalExerciseName': testexercise3.external_exercise_name,
                    'externalExerciseBodypart': testexercise3.external_exercise_bodypart,
                    'personalBest': testexercise3.personal_best,
                    'userId': {'userId': str(testuserjill.user_id), 'username': testuserjill.username}
            }
            ]
                
        }
    }

@pytest.mark.django_db
def test_get_all_workouts_is_empty():


    query = '''
       query {
            getAllWorkouts {
                reps
                sets
                weightKg
                workoutId
                exerciseId {
                    exerciseId
                    externalExerciseName
                    userId {
                        userId
                        username
                }
                }
               
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed == {
        'data': {
            'getAllWorkouts': []
                },
    }


@pytest.mark.django_db
def test_get_all_workouts():

    testuserjames = User.objects.create(username='jamesgains')

    workoutexercise = Exercise.objects.create(user_id=testuserjames, external_exercise_id='1304', external_exercise_name='Glute Bridge Test', external_exercise_bodypart='Upper Legs', personal_best=20)
    testworkout = WorkoutLog.objects.create(exercise_id=workoutexercise, reps= 12, sets=3, weight_kg=20)

    query = '''
       query {
            getAllWorkouts {
                reps
                sets
                weightKg
                workoutId
                exerciseId {
                    exerciseId
                    externalExerciseName
                    userId {
                        userId
                        username
                }
                }
               
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed == {
        'data': {
            'getAllWorkouts': [{
                'exerciseId': {'exerciseId': str(workoutexercise.exercise_id),
                               'externalExerciseName': workoutexercise.external_exercise_name,
                               'userId': {
                                   'userId': str(testuserjames.user_id),
                                   'username': testuserjames.username
                               }
                               },
                'reps': testworkout.reps,
                'sets': testworkout.sets,
                'weightKg': testworkout.weight_kg,
                'workoutId': str(testworkout.workout_id)
                }]
                },
    }
