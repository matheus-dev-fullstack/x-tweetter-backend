from django.forms import ValidationError
from rest_framework import serializers
from posts.models import Post, Imagem, Like, Comentarios
from usuarios.serializers import PerfilSerializer


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
    author = PerfilSerializer(read_only=True)
    # imagens = ImagemSerializer(many=True)
    likes = LikeSerializer(many=True, read_only=True)
    comentarios = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'content', 'released', 'author', 'likes', 'comentarios']
        # fields = ['id', 'content', 'released', 'author', 'imagens', 'likes', 'comentarios']
        # fields = ['id', 'content', 'released', 'author', 'imagens', 'likes', 'comentarios']
        
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        
        if user is None or not user.is_authenticated:
            raise ValidationError("Usuário não autenticado. O post não pode ser criado.")
        
        # imagens_data = validated_data.pop('imagens', [])
        post = Post.objects.create(author=user, **validated_data)
        
        # for image_data in imagens_data:
        #     Imagem.objects.create(post=post, **image_data)
        
        return post

class PostSummarySerializer(serializers.ModelSerializer):
    # likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    # comments_count = serializers.IntegerField(source='comentarios.count', read_only=True)

    class Meta:
        model = Post
        # fields = ['id', 'content', 'author', 'released', 'likes_count', 'comments_count']
        fields = ['id', 'content', 'author', 'released']