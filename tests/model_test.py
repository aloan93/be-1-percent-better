import pytest
from api.models import User

@pytest.mark.django_db
def test_user_model():
    # Creates a new user in the database
    user = User.objects.create(username='testuser')
    # Fetch the User instance from the database 
    queried_user = User.objects.get(username='testuser')
    # Assertions check the username matches the expacted value
    assert user.username == 'testuser'
    assert queried_user.username == 'testuser'