import pytest
import api.models

@pytest.mark.django_db
def test_user_model():
    # Creates a new user in the database
    user = api.models.User.objects.create(username='testuser')
    # Fetch the User instance from the database 
    queried_user = api.models.User.objects.get(username='testuser')
    # Assertions check the username matches the expacted value
    assert user.username == 'testuser'
    assert queried_user.username == 'testuser'