from django.db import models
from usuarios.models import Usuario
from PIL import Image 

class Post(models.Model):
    content = models.CharField(max_length=300)
    author = models.ForeignKey(Usuario,  on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='posts_images/', blank=True, null=True)
    released = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author} postou {self.content}'
    
class Like(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user.name} liked {self.post.id}'


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    author = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.name} commented on {self.post.id}'