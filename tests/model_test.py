import pytest
from api.models import User, Exercise, SessionLog, WorkoutLog, SessionLog_Exercise

@pytest.mark.django_db
def test_user_model():
    # Creates a new user in the database
    user = User.objects.create(username='testuser')
    # Fetch the User instance from the database
    queried_user = User.objects.get(username='testuser')
    # Assertions check the username matches the expected value
    assert user.username == 'testuser', "Username does not match the expected value."
    assert queried_user.username == 'testuser', "Username does not match the expected value."

@pytest.mark.django_db
def test_create_exercise():
    # Create user
    user = User.objects.create(username='testuser')
    # Create Exercise
    exercise = Exercise.objects.create(user_id=user, external_exercise_id='1234', external_exercise_name='Squat', external_exercise_bodypart='Legs', personal_best=0)
    # Check how many exercise instances are in the database / Error message 
    assert Exercise.objects.count() == 1, "Number of exercises in the database does not match the expected value."
    # Check exercise name / Error message
    assert exercise.external_exercise_name == 'Squat', "Exercise name does not match the expected value."
    # Check username related to exercise 
    assert exercise.user_id.username == 'testuser', "Exercise's user username does not match the expected value."

@pytest.mark.django_db
def test_create_workout_log():
    user = User.objects.create(username='testuser')
    exercise = Exercise.objects.create(user_id=user, external_exercise_id='1234', external_exercise_name='Squat', external_exercise_bodypart='Legs', personal_best=0)
    workout_log = WorkoutLog.objects.create(exercise_id=exercise, reps=10, weight_kg=20, sets=3)
    assert WorkoutLog.objects.count() == 1, "Number of workout logs in the database does not match the expected value."
    assert workout_log.exercise_id.external_exercise_name == 'Squat', "Workout log's exercise name does not match the expected value."
    assert workout_log.exercise_id.user_id.username == 'testuser', "Exercise's user username does not match the expected value."

@pytest.mark.django_db
def test_create_session_log():
    user = User.objects.create(username='testuser')
    session_log = SessionLog.objects.create(user_id=user, session_name='Test Session')
    assert SessionLog.objects.count() == 1, "Number of session logs in the database does not match the expected value."
    assert session_log.session_name == 'Test Session', "Session log's name does not match the expected value."
    assert session_log.user_id.username == 'testuser', "Exercise's user username does not match the expected value."

@pytest.mark.django_db
def test_create_session_log_exercise():
    user = User.objects.create(username='testuser')
    exercise = Exercise.objects.create(user_id=user, external_exercise_id='1234', external_exercise_name='Squat', external_exercise_bodypart='Legs', personal_best=0)
    session_log = SessionLog.objects.create(user_id=user, session_name='Test Session')
    session_log_exercise = SessionLog_Exercise.objects.create(session_id=session_log, exercise_id=exercise)
    assert SessionLog_Exercise.objects.count() == 1, "Number of session log exercises does not match the expected value."
    assert session_log_exercise.exercise_id.external_exercise_name == 'Squat', "Session log exercise's name does not match the expected value."
    assert session_log_exercise.session_id.session_name == 'Test Session', "Session log exercise's session name does not match the expected value."
    assert session_log_exercise.session_id.user_id.username == 'testuser', "Exercise's user username does not match the expected value."

