from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.create_user(username = request.data.get("username"), 
                                        email= request.data.get("email"),
                                        password=request.data.get("password"))
        user.save()
        return Response(
            {
            'user_id': user.pk,
            'email': user.email
            }
        )
        
