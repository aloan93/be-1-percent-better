from graphene.test import Client
from api.schema import schema
from api.models import User, Exercise
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

