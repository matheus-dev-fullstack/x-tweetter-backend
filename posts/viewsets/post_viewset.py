from rest_framework import viewsets
from posts.models import Post, Imagem, Like, Comentarios
from posts.serializers import PostSerializer, ImagemSerializer, LikeSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all().order_by('-released')
    serializer_class = PostSerializer
    
class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer
    
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comentarios.objects.all()
    serializer_class = CommentSerializer