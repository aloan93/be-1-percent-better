import graphene
from graphene_django import DjangoObjectType 
from .models import User, Exercise, WorkoutLog, SessionLog, SessionLog_Exercise

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class Query(graphene.ObjectType):

    get_all_users = graphene.List(UserType)

    def resolve_get_all_users(self, info):
            return User.objects.all()
    
schema = graphene.Schema(query=Query)