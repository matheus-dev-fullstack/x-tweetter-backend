from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from posts.models import Post, Like, Comentario
from posts.serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import action
import os
from PIL import Image
from django.conf import settings
from usuarios.models import Usuario


class PostViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-released')
    # parser_classes = (JSONParser, MultiPartParser, FormParser)



    def perform_create(self, serializer):
        # imagem = self.request.FILES.get('imagem')
        post = serializer.save(author=self.request.user)
        
    @action(detail=False, methods=['get'], url_path='following-posts', permission_classes=[AllowAny])
    def following_posts(self, request):
        user = request.user
        
        following_users = user.following.all()
        
        posts = Post.objects.filter(author__in=following_users).order_by('-released')
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'], url_path='user-posts/(?P<username>[^/.]+)', permission_classes=[AllowAny])
    def user_posts(self, request, username=None):
        try:
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(author=user).order_by('-released')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        if Like.objects.filter(post=post, user=user).exists():
            return Response({"detail": "Você já curtiu este post."}, status=400)
        
        Like.objects.create(post=post, user=user)
        return Response({'status': 'like adicionado'}, status=status.HTTP_201_CREATED)
        
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request, 'post': post}    )

        if serializer.is_valid():
            serializer.save(post=post, author=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError("Post não encontrado para associar ao comentário.")

        serializer.save(author=self.request.user, post=post)