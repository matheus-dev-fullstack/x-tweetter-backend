from django.shortcuts import get_object_or_404
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
    queryset = Usuario.objects.all()
    serializer_class = PerfilSerializer
    
    def list(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'], url_path='editar-perfil', permission_classes=[AllowAny])
    def editar_perfil(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Perfil atualizado com sucesso!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='overview/(?P<username>[^/.]+)')
    def perfil_overview(self, request, username=None):
        user = get_object_or_404(Usuario, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def follow(self, request, pk=None):
        user_to_follow = get_object_or_404(Usuario, pk=pk)
        user = request.user

        if user == user_to_follow:
            return Response({"message": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        if user_to_follow.followers.filter(id=user.id).exists():
            return Response({"message": "Você já está seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)

        user_to_follow.followers.add(user)
        return Response({"message": f"Agora você está seguindo {user_to_follow.username}."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        user_to_unfollow = get_object_or_404(Usuario, pk=pk)
        user = request.user

        if user_to_unfollow.followers.filter(id=user.id).exists():
            user_to_unfollow.followers.remove(user)
            return Response({"message": f"Você deixou de seguir {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
        
        return Response({"message": "Você não está seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def followers(self, request, pk=None):
        
        user = get_object_or_404(Usuario, pk=pk)
        followers = user.followers.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def following(self, request, pk=None):
        user = get_object_or_404(Usuario, pk=pk)
        following = user.following.all()
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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