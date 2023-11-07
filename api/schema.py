import graphene
from graphene_django import DjangoObjectType 
from .models import User, Exercise, WorkoutLog, SessionLog, SessionLog_Exercise

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):

    get_all_users = graphene.List(UserType)
    get_user_by_id = graphene.Field(UserType, user_id=graphene.Int())


    def resolve_get_all_users(self, info):
        return User.objects.all()
    
    def resolve_get_user_by_id(self, info, user_id):
        return User.objects.get(pk=user_id)
         

schema = graphene.Schema(query=Query)