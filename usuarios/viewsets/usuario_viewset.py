from rest_framework import viewsets,status
from posts.models import  Usuario
from posts.serializers import UsuarioSerializer
from usuarios.serializers import  LoginTokenSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate




class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    
    
# class LoginViewSet(viewsets.ViewSet):

#     @action(detail=False, methods=['post'])
#     def authenticate(self, request):
#         serializer = LoginTokenSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             return Response({"message": "Login bem-sucedido!", "username": user.username}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def authenticate(self, request):
        serializer = LoginTokenSerializer(data=request.data)
        if serializer.is_valid():
            token_data = serializer.validated_data
            return Response({
                "message": "Login bem-sucedido!",
                "access_token": token_data['access'],
                "refresh_token": token_data['refresh']
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)