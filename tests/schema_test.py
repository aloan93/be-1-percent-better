from graphene.test import Client
from api.schema import schema
from api.models import User, Exercise, WorkoutLog, SessionLog
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

