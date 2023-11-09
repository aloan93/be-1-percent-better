from graphene.test import Client
from api.schema import schema
from api.models import User, Exercise, WorkoutLog, SessionLog
import pytest

@pytest.mark.django_db
def test_get_all_users():
  
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
   
    query = '''
        query {
            getAllUsers {
                userId
                username
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
    
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
                getUserByUserId(userId: 10) {
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
def test_get_users_by_nonexistent_user_id():
    
   
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
    
  
    assert executed['data'] ==  {'getUserByUserId': None}

    assert executed['errors'] == [{
        'locations': [{
                        'column': 17,
                        'line': 3}],
            'message': 'User matching query does not exist.',
            'path': ['getUserByUserId']}]
    

@pytest.mark.django_db
def test_get_users_by_invalid_string_user_id():
    
   
    query = '''
       query {
                getUserByUserId(userId: banana) {
                    userId
                    username
            }
        }
    '''
    
    client = Client(schema)
    
    executed = client.execute(query)
    
  
    assert executed['data'] == None
    assert executed['errors'] == [{
            'locations': [{
                'column': 41,
                'line': 3}],
            'message': "Int cannot represent non-integer value: banana"
    }]

@pytest.mark.django_db
def test_get_exercise_by_exercise_id():

    testuserjim = User.objects.create(username='jimsgains')
    testexercise = Exercise.objects.create(user_id=testuserjim, external_exercise_id='1004', external_exercise_name='Leg Press', external_exercise_bodypart='Lower Legs', personal_best=0)
   
    query = '''
       query {
            getExerciseByExerciseId(exerciseId: 6) {
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
def test_get_exercise_by_nonexistent_exercise_id():

    query = '''
       query {
            getExerciseByExerciseId(exerciseId: 60004) {
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
  
    assert executed['data'] == {'getExerciseByExerciseId': None}
    assert executed['errors'] == [{'locations': [{'column': 13,
                                                  'line': 3}],
                                    'message': 'Exercise matching query does not exist.',
                                    'path': ['getExerciseByExerciseId']}] 

@pytest.mark.django_db
def test_get_exercise_by_invalid_string_exercise_id():

    query = '''
       query {
            getExerciseByExerciseId(exerciseId: '4397584395') {
                exerciseId
                externalExerciseId
                userId {
                    userId
                    username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed['data'] == None
    assert executed['errors'] == [{'locations': [{
                                        'column': 49,
                                        'line': 3}],
                                    'message': "Syntax Error: Unexpected single quote character ('), did you " 'mean to use a double quote (")?'},
                                    ]


@pytest.mark.django_db
def test_get_exercise_by_invalid_double_string_exercise_id():

    query = '''
       query {
            getExerciseByExerciseId(exerciseId: "43975") {
                exerciseId
                externalExerciseId
                userId {
                    userId
                    username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed['data'] == None
    assert executed['errors'] == [{'locations': [{
                                        'column': 49,
                                        'line': 3}],
                                    'message': 'Int cannot represent non-integer value: "43975"'
                                    },
                                    ]

@pytest.mark.django_db
def test_get_exercise_by_boolean_exercise_id():

    query = '''
       query {
            getExerciseByExerciseId(exerciseId: True) {
                exerciseId
                externalExerciseId
                userId {
                    userId
                    username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed['data'] == None
    assert executed['errors'] == [{'locations': [{
                                        'column': 49,
                                        'line': 3}],
                                    'message': 'Int cannot represent non-integer value: True'
                                    },
                                    ]

@pytest.mark.django_db
def test_get_exercise_by_blank_exercise_id():

    query = '''
       query {
            getExerciseByExerciseId(exerciseId: ) {
                exerciseId
                externalExerciseId
                userId {
                    userId
                    username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed['data'] == None
    assert executed['errors'] == [{'locations': [{
                                        'column': 49,
                                        'line': 3}],
                                    'message': "Syntax Error: Unexpected ')'."
                                    },
                                    ]

@pytest.mark.django_db
def test_get_exercises_by_user_id():

    testuserjill = User.objects.create(username='jillsgains')

    testexercise = Exercise.objects.create(user_id=testuserjill, external_exercise_id='1004', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=10)
    testexercise2 = Exercise.objects.create(user_id=testuserjill, external_exercise_id='1024', external_exercise_name='Sumo Squat', external_exercise_bodypart='Upper Legs', personal_best=10)
    testexercise3 = Exercise.objects.create(user_id=testuserjill, external_exercise_id='1324', external_exercise_name='Romanian Deadlift', external_exercise_bodypart='Upper Legs', personal_best=20)

    query = '''
       query {
            getExercisesByUserId(userId: 12) {
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
def test_get_exercises_by_nonexistent_user_id():  
   
    query = '''
       query {
                getExercisesByUserId(userId: 344) {
                    exerciseId
                    userId {
                        userId
                        username
                    }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(query)
    
  
    assert executed['data'] == {'getExercisesByUserId': []} 

@pytest.mark.django_db
def test_get_exercises_by_invalid_string_user_id():
    
    query = '''
       query {
                getExercisesByUserId(userId: banana) {
                    exerciseId
                    userId {
                        userId
                        username
                    }
            }
        }
    '''
    
    client = Client(schema)
    
    executed = client.execute(query)
    
  
    assert executed['data'] == None
    assert executed['errors'] == [{
            'locations': [{
                'column': 46,
                'line': 3}],
            'message': "Int cannot represent non-integer value: banana"
    }]
    

@pytest.mark.django_db
def test_get_all_sessions_is_empty():

    query = '''
        query {
              getAllSessions {
                    sessionId
                    sessionName
                    userId {
                        userId
                        username
                    }
            }
        }
        '''
       
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed['data'] == {'getAllSessions': []}

@pytest.mark.django_db
def test_get_all_sessions():

    testusercraig = User.objects.create(username='craigsgains')

    testsession = SessionLog.objects.create(user_id=testusercraig, session_name="Leg Day")

    query = '''
        query {
              getAllSessions {
                    sessionId
                    sessionName
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
        'data':  {'getAllSessions': [{
                        'sessionId': str(testsession.session_id),
                        'sessionName': testsession.session_name,
                        'userId': {
                            'userId': str(testusercraig.user_id),
                            'username': testusercraig.username
                            }
                        }]
                    },
    }

@pytest.mark.django_db
def test_get_sessions_by_user_id():

    testuser = User.objects.create(username="testing")

    testsession = SessionLog.objects.create(user_id=testuser, session_name="Test Chest Day")

    query = '''
        query {
              getSessionsByUserId(userId: 14) {
                    sessionId
                    sessionName
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
        'data':  {'getSessionsByUserId': [{
                        'sessionId': str(testsession.session_id),
                        'sessionName': testsession.session_name,
                        'userId': {
                            'userId': str(testuser.user_id),
                            'username': testuser.username
                            }
                        }]
                    },
    }

@pytest.mark.django_db
def test_get_sessions_by_nonexistent_user_id():

    query = '''
        query {
              getSessionsByUserId(userId: 555555) {
                    sessionId
                    sessionName
                    userId {
                        userId
                        username
                    }
                }
            }
        '''
       
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed['data'] == {'getSessionsByUserId': []}

@pytest.mark.django_db
def test_get_sessions_by_invalid_user_id():

    query = '''
        query {
              getSessionsByUserId(userId: "banana") {
                    sessionId
                    sessionName
                    userId {
                        userId
                        username
                    }
                }
            }
        '''
       
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed['data'] == None
    assert executed['errors'] == [{'locations': [{'column': 43, 'line': 3}], 'message': 'Int cannot represent non-integer value: "banana"'}]

@pytest.mark.django_db
def test_get_session_by_session_id():

    testuser = User.objects.create(username="testing")
    testsession = SessionLog.objects.create(user_id=testuser, session_name="Test Leg Day")

    query = '''
        query {
              getSessionBySessionId(sessionId: 5) {
                    sessionId
                    sessionName
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
        'data':  {'getSessionBySessionId': {
                        'sessionId': str(testsession.session_id),
                        'sessionName': testsession.session_name,
                        'userId': {
                            'userId': str(testuser.user_id),
                            'username': testuser.username
                            }
                        }
                    },
    }

@pytest.mark.django_db
def test_get_session_by_nonexistent_session_id():

    query = '''
        query {
              getSessionBySessionId(sessionId: 555555) {
                    sessionId
                    sessionName
                    userId {
                        userId
                        username
                    }
                }
            }
        '''
       
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed['data'] == {'getSessionBySessionId': None}
    assert executed['errors'] == [{
                    'locations': [{'column': 15,
                                   'line': 3}],
                    'message': 'SessionLog matching query does not exist.',
                    'path': ['getSessionBySessionId']
    }]
    

@pytest.mark.django_db
def test_get_session_by_invalid_session_id():

    query = '''
        query {
              getSessionBySessionId(sessionId: "banana") {
                    sessionId
                    sessionName
                    userId {
                        userId
                        username
                    }
                }
            }
        '''
       
    client = Client(schema)
    executed = client.execute(query)
  
    assert executed['data'] == None
    assert executed['errors'] == [{'locations': [{'column': 48, 'line': 3}],
                                    'message':'Int cannot represent non-integer value: "banana"'
                                    }]

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
    me = User.objects.get(username="jamesgains")

    workoutexercise = Exercise.objects.create(user_id=me, external_exercise_id='1304', external_exercise_name='Glute Bridge Test', external_exercise_bodypart='Upper Legs', personal_best=20)
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
                                   'userId': str(me.user_id),
                                   'username': me.username
                               }
                               },
                'reps': testworkout.reps,
                'sets': testworkout.sets,
                'weightKg': testworkout.weight_kg,
                'workoutId': str(testworkout.workout_id)
                }]
                },
    }

@pytest.mark.django_db
def test_get_workout_by_workout_id():

    testuserjane = User.objects.create(username="janesgains")

    workoutexercise = Exercise.objects.create(user_id=testuserjane, external_exercise_id='1304', external_exercise_name='Glute Band Test', external_exercise_bodypart='Upper Legs', personal_best=10)
    testworkout = WorkoutLog.objects.create(exercise_id=workoutexercise, reps= 10, sets=3, weight_kg=10)

    query = '''
        query {
            getWorkoutByWorkoutId(workoutId: 3) {
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
            'getWorkoutByWorkoutId': {
                'exerciseId': {'exerciseId': str(workoutexercise.exercise_id),
                               'externalExerciseName': workoutexercise.external_exercise_name,
                               'userId': {
                                   'userId': str(testuserjane.user_id),
                                   'username': testuserjane.username
                               }
                               },
                'reps': testworkout.reps,
                'sets': testworkout.sets,
                'weightKg': testworkout.weight_kg,
                'workoutId': str(testworkout.workout_id)
                }
                },
    }

@pytest.mark.django_db
def test_get_workout_by_nonexistent_workout_id():

    query = '''
        query {
            getWorkoutByWorkoutId(workoutId: 3000000) {
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
            'getWorkoutByWorkoutId': None
                },
        'errors': [{
            'locations': [{
                'column': 13,
                'line': 3
            }],
            'message': 'WorkoutLog matching query does not exist.',
            'path': ['getWorkoutByWorkoutId'] 
        }]
    }

@pytest.mark.django_db
def test_get_workout_by_invalid_workout_id():

    query = '''
        query {
            getWorkoutByWorkoutId(workoutId: bananas) {
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
        'data': None,
        'errors': [{
            'locations': [{
                'column': 46,
                'line': 3
            }],
            'message': 'Int cannot represent non-integer value: bananas',
        }]
    }

@pytest.mark.django_db
def test_get_workouts_by_exercise_id_empty():

    query = '''
        query {
            getWorkoutsByExerciseId(exerciseId: 11) {
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
            'getWorkoutsByExerciseId': []
                },
    }

@pytest.mark.django_db
def test_get_workouts_by_exercise_id():

    testuserjane = User.objects.create(username="janesgains")

    workoutexercise = Exercise.objects.create(user_id=testuserjane, external_exercise_id='1304', external_exercise_name='Glute Band Test', external_exercise_bodypart='Upper Legs', personal_best=10)
    testworkout = WorkoutLog.objects.create(exercise_id=workoutexercise, reps= 10, sets=3, weight_kg=10)

    query = '''
        query {
            getWorkoutsByExerciseId(exerciseId: 12) {
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
            'getWorkoutsByExerciseId': [{
                'exerciseId': {'exerciseId': str(workoutexercise.exercise_id),
                               'externalExerciseName': workoutexercise.external_exercise_name,
                               'userId': {
                                   'userId': str(testuserjane.user_id),
                                   'username': testuserjane.username
                               }
                               },
                'reps': testworkout.reps,
                'sets': testworkout.sets,
                'weightKg': testworkout.weight_kg,
                'workoutId': str(testworkout.workout_id)
                }]
                },
    }

@pytest.mark.django_db
def test_get_workouts_by_invalid_exercise_id():

    query = '''
        query {
            getWorkoutsByExerciseId(exerciseId: bananas) {
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
        'data': None,
        'errors': [{
            'locations': [{
                'column': 49,
                'line': 3
            }],
            'message': 'Int cannot represent non-integer value: bananas',
        }]
    }

@pytest.mark.django_db
def test_get_workouts_by_nonexistent_exercise_id():

    query = '''
        query {
            getWorkoutsByExerciseId(exerciseId: 3000000) {
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
            'getWorkoutsByExerciseId': []
                },
    }

@pytest.mark.django_db
def test_create_user():

    mutation = '''
        mutation  {
            createUser(username: "test") {
                user {
                userId
                username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(mutation)
  
    assert executed == {
        'data': {
            'createUser': {
                'user': {
                    'userId': '19',
                    'username': 'test'
                }
                
            }
        }
    }

@pytest.mark.django_db
def test_create_invalid_user():

    mutation = '''
        mutation  {
            createUser(username: test) {
                user {
                userId
                username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(mutation)
  
    assert executed == {
        'data': None,
        'errors': [{'locations': [{
                        'column': 34,
                        'line':3
                        }],
                    'message': 'String cannot represent a non string value: test'
                    }]
        }

@pytest.mark.django_db
def test_update_user_username():

    testuserjane = User.objects.create(username="janesgains")

    mutation = '''
        mutation  {
            updateUser(userId: "20", username: "testupdate") {
                user {
                userId
                username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(mutation)
  
    assert executed == {
        'data': {
            'updateUser': {
                'user': {
                    'userId': '20',
                    'username': 'testupdate'
                }
                
            }
        }
    }

@pytest.mark.django_db
def test_update_nonexistent_user_username():

    mutation = '''
        mutation  {
            updateUser(userId: "200000", username: "testupdate") {
                user {
                userId
                username
                }
            }
        }
    '''
    
    client = Client(schema)
    executed = client.execute(mutation)
  
    assert executed == {
        'data': {'updateUser': None},
        'errors': [{'locations': [{'column': 13,
                                   'line': 3
                                    }],
                    'message': 'User matching query does not exist.',
                    'path': ['updateUser'],
                    }]
        }
    
    invalidmutation = '''
        mutation  {
            updateUser(userId: "200000", username: testupdate) {
                user {
                userId
                username
                }
            }
        }
    '''
    
    client = Client(schema)
    executedinvalid = client.execute(invalidmutation)
  
    assert executedinvalid == {
        'data': None,
        'errors': [{'locations': [{'column': 52,
                                   'line': 3
                                    }],
                    'message': 'String cannot represent a non string value: ' 'testupdate',
                    }]
        }

@pytest.mark.django_db
def test_delete_user_username():

    testuserjane = User.objects.create(username="janesgains")

    mutation = '''
        mutation  {  
            deleteUser(userId: "21") {
                user {
                    userId
                    username
                }
            }
        }
    '''
    
    query = '''
        query {
            getAllUsers {
                userId
                username
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(query)
    client.execute(mutation)
    deleted = client.execute(query)
  
    assert executed == {'data': {'getAllUsers': [{'userId': '21', 'username': 'janesgains'}]}}
    assert deleted == {'data': {'getAllUsers': []}}


@pytest.mark.django_db
def test_create_exercise():

    testuserjane = User.objects.create(username="janesgains")

    mutation = '''
        mutation  {
            createExercise(
                externalExerciseBodypart: "waist"
                externalExerciseId: "2000"
                externalExerciseName: "chest press"
                userId: "22"
            ) {
            exercise {
                exerciseId
                externalExerciseBodypart
                externalExerciseId
                externalExerciseName
                personalBest
                userId {
                    userId
                    username
                    }
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    data = executed['data']

    assert data['createExercise'] == {'exercise': 
                                      {'exerciseId': '13', 
                                       'externalExerciseBodypart': 'waist',
                                        'externalExerciseId': '2000', 
                                        'externalExerciseName': 'chest press',
                                        'personalBest': 0,
                                         'userId':{
                                             'userId':'22',
                                             'username': 'janesgains'
                                            }
                                        }
                                    }


@pytest.mark.django_db
def test_create_exercise_no_user():

    mutation = '''
        mutation  {
            createExercise(
                externalExerciseBodypart: "waist"
                externalExerciseId: "2000"
                externalExerciseName: "chest press"
            ) {
            exercise {
                exerciseId
                externalExerciseBodypart
                userId {
                    userId
                    username
                    }
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': None,
                        'errors': [{
                            'locations': [{
                                'column': 13,
                                'line': 3
                                }],
                            'message': "Field 'createExercise' argument 'userId' of type " 
                                        "'ID!' is required, but it was not provided."
                        }]}

@pytest.mark.django_db
def test_create_exercise_nonexistent_user():

    testuserjane = User.objects.create(username="janesgains")

    mutation = '''
        mutation  {
            createExercise(
                externalExerciseBodypart: "waist"
                externalExerciseId: "2000"
                externalExerciseName: "chest press"
                userId: "499999"
            ) {
            exercise {
                exerciseId
                externalExerciseBodypart
                userId {
                    userId
                    username
                    }
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)

    assert executed == {'data': {'createExercise': None},
                        'errors': [{
                            'locations': [{
                                'column': 13,
                                'line': 3
                                }],
                            'message': 'User matching query does not exist.',
                            'path': ['createExercise']
                        }]}
    
@pytest.mark.django_db
def test_update_exercise():

    testuser = User.objects.create(username="tester")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    mutation = '''
        mutation {
            updateExercise(exerciseId: "14", personalBest: 50) {
                exercise {
                exerciseId
                personalBest
                externalExerciseName
                externalExerciseId
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': {'updateExercise': {
                                    'exercise': {
                                        'exerciseId':str(testexercise.exercise_id),
                                        'externalExerciseId': str(testexercise.external_exercise_id),
                                        'externalExerciseName': testexercise.external_exercise_name,
                                        'personalBest': 50
                                        }}
                                    }  
    }

@pytest.mark.django_db
def test_update_exercise_nonexistent_exercise_id():

    testuser = User.objects.create(username="tester")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    mutation = '''
        mutation {
            updateExercise(exerciseId: "1200", personalBest: 50) {
                exercise {
                exerciseId
                personalBest
                externalExerciseName
                externalExerciseId
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': {'updateExercise': None },  
                        'errors': [{'locations': [{'column': 13,
                                                   'line': 3
                                                   }],
                                    'message': 'Exercise matching query does not exist.',
                                    'path': ['updateExercise']
                                    }]
    }


@pytest.mark.django_db
def test_update_exercise_without_pb():

    testuser = User.objects.create(username="tester")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    mutation = '''
        mutation {
            updateExercise(exerciseId: "1200") {
                exercise {
                exerciseId
                personalBest
                externalExerciseName
                externalExerciseId
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': None,  
                        'errors': [{'locations': [{'column': 13,
                                                   'line': 3
                                                   }],
                                    'message': "Field 'updateExercise' argument 'personalBest' of " 
                                                "type 'Int!' is required, but it was not provided."
                                    }]
    }

@pytest.mark.django_db
def test_update_exercise_invalid_pb():

    testuser = User.objects.create(username="tester")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    mutation = '''
        mutation {
            updateExercise(exerciseId: "1200", personalBest: "90") {
                exercise {
                exerciseId
                personalBest
                externalExerciseName
                externalExerciseId
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': None,  
                        'errors': [{'locations': [{'column': 62,
                                                   'line': 3
                                                   }],
                                    'message': 'Int cannot represent non-integer value: "90"'
                                    }]
    }

@pytest.mark.django_db
def test_delete_exercise():

    testuser = User.objects.create(username="janesgains")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    query = '''
        query {
            getAllExercises {
                userId {
                    username
                }
                exerciseId
            }
        }
    '''

    mutation = '''
        mutation  {  
            deleteExercise(exerciseId: "18") {
                exercise {
                    exerciseId
                    }
                }
        }
    '''

    client = Client(schema)
    executed = client.execute(query)

    assert executed == {'data': {'getAllExercises': [{'exerciseId': str(testexercise.exercise_id), 'userId': {'username': 'janesgains'}}]}}

    client.execute(mutation)
    deleted = client.execute(query)
  
    assert deleted == {'data': {'getAllExercises': []}}

@pytest.mark.django_db
def test_delete_exercise_nonexistent_id():

    testuser = User.objects.create(username="janesgains")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    query = '''
        query {
            getAllExercises {
                userId {
                    username
                }
                exerciseId
            }
        }
    '''

    mutation = '''
        mutation  {  
            deleteExercise(exerciseId: "180") {
                exercise {
                    exerciseId
                    }
                }
        }
    '''

    client = Client(schema)
    executed = client.execute(query)

    assert executed == {'data': {'getAllExercises': [{'exerciseId': str(testexercise.exercise_id), 'userId': {'username': 'janesgains'}}]}}

    client.execute(mutation)
    deleted = client.execute(mutation)
  
    assert deleted == {'data': {'deleteExercise': None},
                       'errors': [{'locations': [{'column': 13,
                                                  'line': 3}],
                                    'message': 'Exercise matching query does not exist.',
                                    'path': ['deleteExercise']
                                    }]
                        }  

@pytest.mark.django_db
def test_create_workout():

    testuserjane = User.objects.create(username="janesgains")
    testexercise = Exercise.objects.create(user_id=testuserjane, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    mutation = '''
        mutation  {
            createWorkout(exerciseId: "20", reps: 10, sets: 12, weightKg: 15) {
                workout {
                reps
                sets
                weightKg
                workoutId
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': {
                           'createWorkout': {
                                'workout': {
                                    'reps': 10,
                                    'sets': 12,
                                    'weightKg': 15,
                                    'workoutId': '5'
                                    }
                                }
                            }
    } 

@pytest.mark.django_db
def test_create_workout_fail_missing_id():

    testuserjane = User.objects.create(username="janesgains")
    testexercise = Exercise.objects.create(user_id=testuserjane, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    mutation = '''
        mutation  {
            createWorkout(reps: 10, sets: 12, weightKg: 15) {
                workout {
                reps
                sets
                weightKg
                workoutId
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': None,
                        'errors': [{'locations': [{'column': 13, 'line': 3}],
                        'message': "Field 'createWorkout' argument 'exerciseId' of type "
                                     "'ID!' is required, but it was not provided."}],       
    } 

@pytest.mark.django_db
def test_create_workout_fail_missing_fields():

    testuserjane = User.objects.create(username="janesgains")
    testexercise = Exercise.objects.create(user_id=testuserjane, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    missingsets = '''
        mutation  {
            createWorkout(exerciseId: "21", reps: 12, weightKg: 15) {
                workout {
                reps
                sets
                weightKg
                workoutId
                }
            }
        }
    '''

    client = Client(schema)
    executednosets = client.execute(missingsets)

    assert executednosets == {'data': None,
                              'errors': [{'locations': [{'column': 13, 
                                                         'line': 3}],
                                          'message': "Field 'createWorkout' argument 'sets' of type 'Int!' "
                                                     'is required, but it was not provided.'}],     
                            }

    missingreps = '''
        mutation  {
            createWorkout(exerciseId: "21", sets: 12, weightKg: 15) {
                workout {
                reps
                sets
                weightKg
                workoutId
                }
            }
        }
    '''
    executednoreps = client.execute(missingreps)

    assert executednoreps == {'data': None,
                              'errors': [{'locations': [{'column': 13, 
                                                         'line': 3}],
                                          'message': "Field 'createWorkout' argument 'reps' of type 'Int!' "
                                                     'is required, but it was not provided.'}],                         
                            }

    missingweight = '''
        mutation  {
            createWorkout(exerciseId: "21", sets: 12, reps: 15) {
                workout {
                reps
                sets
                weightKg
                workoutId
                }
            }
        }
    '''
    executednoweight = client.execute(missingweight)

    assert executednoweight == {'data': None,
                              'errors': [{'locations': [{'column': 13, 
                                                         'line': 3}],
                                          'message': "Field 'createWorkout' argument 'weightKg' of type 'Int!' "
                                                     'is required, but it was not provided.'}],                         
                            }
   
@pytest.mark.django_db
def test_update_workout():

    testuser = User.objects.create(username="tester")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)
    testworkout = WorkoutLog.objects.create(exercise_id=testexercise, reps= 10, sets=3, weight_kg=10)

    mutation = '''
        mutation {
            updateWorkout(workoutId: "6", reps: 20, sets: 20, weightKg: 20) {
                workout {
                    workoutId
                    reps
                    sets
                    weightKg
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': {'updateWorkout': {
                                    'workout': {
                                        'workoutId':str(testworkout.workout_id),
                                        'sets': 20,
                                        'weightKg': 20,
                                        'reps': 20
                                        }}
                                    }  
    }

@pytest.mark.django_db
def test_update_workout_fail_no_sets():

    testuser = User.objects.create(username="tester")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)
    testworkout = WorkoutLog.objects.create(exercise_id=testexercise, reps= 10, sets=3, weight_kg=10)

    mutation = '''
        mutation {
            updateWorkout(workoutId: "7", reps: 20, weightKg: 20) {
                workout {
                    workoutId
                    reps
                    sets
                    weightKg
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': None,
                         'errors': [{'locations': [{'column': 13, 'line': 3}],
                         'message': "Field 'updateWorkout' argument 'sets' of type 'Int!' "
                                 'is required, but it was not provided.'}]
                        }

@pytest.mark.django_db
def test_update_workout_fail_nonexistent_id():

    mutation = '''
        mutation {
            updateWorkout(workoutId: "71", reps: 20, weightKg: 20, sets: 100) {
                workout {
                    workoutId
                    reps
                    sets
                    weightKg
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': {'updateWorkout': None},
                          'errors': [{'locations': [{'column': 13, 'line': 3}], 
                                      'message': 'WorkoutLog matching query does not exist.', 
                                      'path': ['updateWorkout']}]}

@pytest.mark.django_db
def test_delete_workout():

    testuser = User.objects.create(username="janesgains")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)
    testworkout = WorkoutLog.objects.create(exercise_id=testexercise, reps= 10, sets=3, weight_kg=10)
    
    query = '''
        query {
            getAllWorkouts {
                workoutId
            }
        }
    '''

    mutation = '''
        mutation  {  
            deleteWorkout(workoutId: "8") {
                workout {
                    workoutId
                    }
                }
        }
    '''

    client = Client(schema)
    executed = client.execute(query)

    assert executed == {'data': {'getAllWorkouts': [{'workoutId': str(testworkout.workout_id)}]}}

    client.execute(mutation)
    deleted = client.execute(query)
  
    assert deleted == {'data': {'getAllWorkouts': []}}

@pytest.mark.django_db
def test_delete_workout_nonexistent_id():

    testuser = User.objects.create(username="janesgains")
    testexercise = Exercise.objects.create(user_id=testuser, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)
    testworkout = WorkoutLog.objects.create(exercise_id=testexercise, reps= 10, sets=3, weight_kg=10)

    mutation = '''
        mutation  {  
            deleteWorkout(workoutId: "180000") {
                workout {
                    workoutId
                    }
                }
        }
    '''

    client = Client(schema)
   
    client.execute(mutation)
    deleted = client.execute(mutation)
  
    assert deleted == {'data': {'deleteWorkout': None},
                       'errors': [{'locations': [{'column': 13, 'line': 3}],
                                   'message': 'WorkoutLog matching query does not exist.',
                                   'path': ['deleteWorkout']}]
                       }

@pytest.mark.django_db
def test_create_session():

    testuserjane = User.objects.create(username="janesgains")
    
    mutation = '''
        mutation  {
            createSession(sessionName: "Leg Day", userId: "37") {
                session {
                    sessionName
                    sessionId
                    }
                }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': {
                           'createSession': {
                                'session': {
                                    'sessionName': 'Leg Day',
                                    'sessionId': '6'
                                    }
                                }
                            }
    } 

@pytest.mark.django_db
def test_create_session_nonexistent_id():
    
    mutation = '''
        mutation  {
            createSession(sessionName: "Leg Day", userId: "36000") {
                session {
                    sessionName
                    sessionId
                    }
                }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': {'createSession': None},
                        'errors': [{'locations': [{'column': 13,
                                                   'line': 3}],
                                     'message': 'User matching query does not exist.',
                                     'path': ['createSession']}],
    } 

@pytest.mark.django_db
def test_update_session():
    
    testuserjane = User.objects.create(username="janesgains")
    testsession = SessionLog.objects.create(user_id=testuserjane, session_name="Test Leg Day")

    mutation = '''
        mutation  {
             updateSession(sessionId: "7", sessionName: "Test Update Leg Day") {
                session {
                    sessionId
                    sessionName
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': {
                           'updateSession': {
                                'session': {
                                    'sessionName': 'Test Update Leg Day',
                                    'sessionId': '7'
                                    }
                                }
                            }
    } 

@pytest.mark.django_db
def test_update_session_invalid_id():
    
    mutation = '''
        mutation  {
             updateSession(sessionId: "7000", sessionName: "Test Update Leg Day") {
                session {
                    sessionId
                    sessionName
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': {'updateSession': None},
                        'errors': [{'locations': [{'column': 14, 'line': 3}],
                                       'message': 'SessionLog matching query does not exist.',
                                       'path': ['updateSession']}]}

@pytest.mark.django_db
def test_update_session_invalid_name():
    
    testuserjane = User.objects.create(username="janesgains")
    testsession = SessionLog.objects.create(user_id=testuserjane, session_name="Test Leg Day")

    mutation = '''
        mutation  {
             updateSession(sessionId: "8", sessionName: 6769606) {
                session {
                    sessionId
                    sessionName
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)
    
    assert executed == {'data': None,
                        'errors': [{'locations': [{'column': 57, 'line': 3}],
                                    'message': 'String cannot represent a non string value: 6769606'}]}


@pytest.mark.django_db
def test_delete_session():

    testuserjane = User.objects.create(username="janesgains")
    testsession = SessionLog.objects.create(user_id=testuserjane, session_name="Test Leg Day")

    query = '''
        query {
            getAllSessions {
                sessionId
            }
        }
    '''

    mutation = '''
        mutation  {  
            deleteSession(sessionId: "9") {
                session {
                    sessionId
                    }
                }
        }
    '''

    client = Client(schema)
    executed = client.execute(query)

    assert executed == {'data': {'getAllSessions': [{'sessionId': '9'}]}}

    client.execute(mutation)
    deleted = client.execute(query)
  
    assert deleted == {'data': {'getAllSessions': []}}

@pytest.mark.django_db
def test_delete_session_fail_nonexistent_id():

    testuserjane = User.objects.create(username="janesgains")
    testsession = SessionLog.objects.create(user_id=testuserjane, session_name="Test Leg Day")

    query = '''
        query {
            getAllSessions {
                sessionId
            }
        }
    '''

    mutation = '''
        mutation  {  
            deleteSession(sessionId: "90000") {
                session {
                    sessionId
                    }
                }
        }
    '''

    client = Client(schema)
    executed = client.execute(query)

    deleted = client.execute(mutation)
  
    assert executed == {'data': {'getAllSessions': [{'sessionId': '10'}]}}
    assert deleted == {'data': {'deleteSession': None},
                       'errors': [{'locations': [{'column': 13, 'line': 3}], 'message': 'SessionLog matching query does not exist.', 'path': ['deleteSession']}]
                       }

@pytest.mark.django_db
def test_create_session_log():
    
    testuserjane = User.objects.create(username="janesgains")
    testsession = SessionLog.objects.create(user_id=testuserjane, session_name="Test Leg Day")
    testexercise = Exercise.objects.create(user_id=testuserjane, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    mutation = '''
        mutation  {  
            createSessionExercise(exerciseId: "27", sessionId: "11") {
                sessionExercise {
                    sessionExerciseId
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(mutation)

    assert executed == {'data': {'createSessionExercise': {'sessionExercise': {'sessionExerciseId': '2'}}}}

@pytest.mark.django_db
def test_create_session_log_fail_nonexistent_ids():
    
    testuserjane = User.objects.create(username="janesgains")
    testsession = SessionLog.objects.create(user_id=testuserjane, session_name="Test Leg Day")
    testexercise = Exercise.objects.create(user_id=testuserjane, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    nonexistentexercise = '''
        mutation  {  
            createSessionExercise(exerciseId: "27000", sessionId: "12") {
                sessionExercise {
                    sessionExerciseId
                }
            }
        }
    '''
    nonexistentsession = '''
        mutation  {  
            createSessionExercise(exerciseId: "28", sessionId: "1200000") {
                sessionExercise {
                    sessionExerciseId
                }
            }
        }
    '''

    client = Client(schema)
    executed = client.execute(nonexistentexercise)

    assert executed == {'data': {'createSessionExercise': None},
                        'errors': [{'message': 'Exercise matching query does not exist.', 'locations': [{'line': 3, 'column': 13}], 'path': ['createSessionExercise']}]}

    executed2 = client.execute(nonexistentsession)

    assert executed2 == {'data': {'createSessionExercise': None},
                         'errors': [{'message': 'SessionLog matching query does not exist.', 'locations': [{'line': 3, 'column': 13}], 'path': ['createSessionExercise']}]}
    
@pytest.mark.django_db
def test_delete_session_exercise():

    testuserjane = User.objects.create(username="janesgains")
    testsession = SessionLog.objects.create(user_id=testuserjane, session_name="Test Leg Day")
    testexercise = Exercise.objects.create(user_id=testuserjane, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    creation = '''
        mutation  {  
            createSessionExercise(exerciseId: "29", sessionId: "13") {
                sessionExercise {
                    sessionExerciseId
                }
            }
        }
    '''

    client = Client(schema)
    created = client.execute(creation)

    assert created == {'data': {'createSessionExercise': {'sessionExercise': {'sessionExerciseId': '3'}}}}

    mutation = '''
        mutation  {  
              deleteSessionExercise(sessionExerciseId: "3") {
                sessionExercise {
                    sessionExerciseId
                    }
                }
            }
    '''

    client = Client(schema)
    executed = client.execute(mutation)

    assert executed == {'data': {'deleteSessionExercise': None}}

@pytest.mark.django_db
def test_delete_session_exercise_fail_nonexistent_id():

    testuserjane = User.objects.create(username="janesgains")
    testsession = SessionLog.objects.create(user_id=testuserjane, session_name="Test Leg Day")
    testexercise = Exercise.objects.create(user_id=testuserjane, external_exercise_id='2104', external_exercise_name='Leg Press', external_exercise_bodypart='Upper Legs', personal_best=0)

    creation = '''
        mutation  {  
            createSessionExercise(exerciseId: "30", sessionId: "14") {
                sessionExercise {
                    sessionExerciseId
                }
            }
        }
    '''

    client = Client(schema)
    created = client.execute(creation)

    assert created == {'data': {'createSessionExercise': {'sessionExercise': {'sessionExerciseId': '4'}}}}

    mutation = '''
        mutation  {  
              deleteSessionExercise(sessionExerciseId: "30000") {
                sessionExercise {
                    sessionExerciseId
                    }
                }
            }
    '''

    client = Client(schema)
    executed = client.execute(mutation)

    assert executed == {'data': {'deleteSessionExercise': None},
                        'errors': [{'locations': [{'column': 15, 'line': 3}],
                                    'message': 'SessionLog_Exercise matching query does not exist.',
                                    'path': ['deleteSessionExercise']}]
                        }