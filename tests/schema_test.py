from graphene.test import Client
from api.schema import schema
from api.models import User
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
    
    # Initialise this client with ethe schema 
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