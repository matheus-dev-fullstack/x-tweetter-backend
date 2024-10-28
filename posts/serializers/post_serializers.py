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
    likes = serializers.SerializerMethodField()
    comentarios = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'content', 'released', 'author', 'likes', 'comentarios']
        
    def get_likes(self, obj):
        return Like.objects.filter(post=obj).count()
    
    def get_comentarios(self, obj):
        return Comentarios.objects.filter(post=obj).count()
        
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
    def add_like(self, post, user):
        if not Like.objects.filter(post=post, user=user).exists():
            Like.objects.create(post=post, user=user)

    def remove_like(self, post, user):
        Like.objects.filter(post=post, user=user).delete()

    def add_comment(self, post, user, content):
        return Comentarios.objects.create(post=post, author=user, content=content)

class PostSummarySerializer(serializers.ModelSerializer):
    # likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    # comments_count = serializers.IntegerField(source='comentarios.count', read_only=True)

    class Meta:
        model = Post
        # fields = ['id', 'content', 'author', 'released', 'likes_count', 'comments_count']
        fields = ['id', 'content', 'author', 'released']