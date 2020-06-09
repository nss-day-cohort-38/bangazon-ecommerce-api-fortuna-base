from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.http import HttpResponseServerError

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )

        fields = ('id', 'first_name', 'last_name', 'url')

class Users(ViewSet):

    def list(self, request):

        users = User.objects.all()

        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

