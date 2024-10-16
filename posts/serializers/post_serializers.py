from rest_framework import serializers
from posts.models import Post, Imagem, Like, Comentarios

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = '__all__'
        # fields = ['id', 'image', 'post']
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post']
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentarios
        fields = ['id', 'post', 'author', 'content', 'created_at']
        
class PostSerializer(serializers.ModelSerializer):
    imagens = ImagemSerializer(many=True)
    likes = LikeSerializer(many=True)
    # comentarios = CommentSerializer(many=True)
    
    class Meta:
        model = Post
        # fields = ['id', 'content', 'released', 'author', 'imagens', 'likes', 'comentarios']
        fields = ['id', 'content', 'released', 'author', 'imagens', 'likes', 'comentarios']

class PostSummarySerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comentarios.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'released', 'likes_count', 'comments_count']