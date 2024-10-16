from django.contrib import admin
from .models import Post, Imagem, Like, Comentarios

# Register your models here.
admin.site.register(Post)
admin.site.register(Imagem)
admin.site.register(Like)
admin.site.register(Comentarios)