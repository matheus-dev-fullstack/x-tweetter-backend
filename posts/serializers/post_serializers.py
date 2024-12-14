from django.forms import ValidationError
from rest_framework import serializers
from posts.models import Post, Like, Comentario
from usuarios.serializers import PerfilSerializer
from PIL import Image


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
            return Comentario.objects.create(post=post, author=author, **validated_data)
        
class PostSerializer(serializers.ModelSerializer):
    # imagens = ImagemSerializer(many=True, required=False)
    # imagem = serializers.ImageField(required=False, allow_null=True)
    
    author = PerfilSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    comentarios = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'content', 'released', 'author', 'likes', 'comentarios', 'imagem']
        read_only_fields =  ['id', 'released', 'author', 'likes', 'comentarios']
        # fields = ['id', 'content', 'released', 'author', 'likes', 'comentarios', 'perfilPhoto']
        
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
        post = super().create(validated_data)

        if post.imagem:
            img = Image.open(post.imagem.path)
            max_size = (700, 700)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(post.imagem.path)

        return post
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user if request else None
        
    #     if user is None or not user.is_authenticated:
    #         raise ValidationError("Usuário não autenticado. O post não pode ser criado.")
        
    #     imagem = validated_data.pop('imagem', None)
    #     post = Post.objects.create(author=user, **validated_data)
        
    #     return post

    # def add_comment(self, post, user, content):
    #     return Comentario.objects.create(post=post, author=user, content=content)