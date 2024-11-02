from django.forms import ValidationError
from rest_framework import serializers
from posts.models import Post, Imagem, Like, Comentario
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
    author = PerfilSerializer(read_only=True)
    class Meta:
        model = Comentario
        fields = ['content', 'post', 'author', 'created_at']
        read_only_fields = [ 'post', 'author', 'created_at']

        def create(self, validated_data):
            post = validated_data.pop('post', None)
            author = validated_data.pop('author', None)
            comentario = Comentario.objects.create(post=post, author=author, **validated_data)
            return comentario
        
class PostSerializer(serializers.ModelSerializer):
    author = PerfilSerializer(read_only=True)
    # imagens = ImagemSerializer(many=True)
    likes = serializers.SerializerMethodField()
    comentarios = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'content', 'released', 'author', 'likes', 'comentarios', 'perfilPhoto']
        
    def get_likes(self, obj):
        return [like.user.id for like in obj.likes.all()]
    
    def get_comentarios(self, obj):
        # return Comentario.objects.filter(post=obj).count()
        comments = Comentario.objects.filter(post=obj)
        comments_data = CommentSerializer(comments, many=True).data
        return {
            "count": comments.count(),
            "details": comments_data
        }
        
        
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

    # def add_comment(self, post, user, content):
    #     return Comentario.objects.create(post=post, author=user, content=content)

class PostSummarySerializer(serializers.ModelSerializer):
    # likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    # comments_count = serializers.IntegerField(source='comentarios.count', read_only=True)

    class Meta:
        model = Post
        # fields = ['id', 'content', 'author', 'released', 'likes_count', 'comments_count']
        fields = ['id', 'content', 'author', 'released']