from rest_framework import viewsets,status
from posts.models import  Usuario
# from posts.serializers import RegisterSerializer
from usuarios.serializers import  LoginTokenSerializer, PerfilSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from usuarios.serializers.usuario_serializers import RegisterSerializer




class PerfilViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = PerfilSerializer
    
    def get_queryset(self):
        return Usuario.objects.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class RegisterViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Usuario.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            token, created = Token.objects.get_or_create(user=user)  
            return Response({
                "message": "Usuário registrado com sucesso!",
                "username": user.username,
                "token": token.key  
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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