from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from posts.models import Post, Imagem, Like, Comentario
from posts.serializers import PostSerializer, ImagemSerializer, LikeSerializer, CommentSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
        
    def get_queryset(self):
        # return Post.objects.select_related('author').all().order_by('-released')
        return Post.objects.prefetch_related('imagens', 'likes', 'comentarios').select_related('author').all().order_by('-released')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        if Like.objects.filter(post=post, user=user).exists():
            Like.objects.filter(post=post, user=user).delete()
            return Response({'status': 'like removido'}, status=status.HTTP_204_NO_CONTENT)
        else:
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
        
    # @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    # def comment(self, request, pk=None):
    #     post = self.get_object()
    #     content = request.data.get('content')
    #     user = request.user
        
    #     if content:
    #         Comentarios.objects.create(post=post, author=user, content=content)
    #         return Response({'status': 'comentario adicionado'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({'status': 'comentário vazio'}, status=status.HTTP_400_BAD_REQUEST)
    
class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer
    permission_classes = [IsAuthenticated]
    
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