from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from posts.models import Post, Imagem, Like, Comentarios
from posts.serializers import PostSerializer, ImagemSerializer, LikeSerializer, CommentSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser) 
    def get_queryset(self):
        # return Post.objects.select_related('author').all().order_by('-released')
        return Post.objects.prefetch_related('imagens', 'likes', 'comentarios').select_related('author').all().order_by('-released')

    
class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer
    permission_classes = [IsAuthenticated]
    
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comentarios.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]