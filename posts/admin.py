from django.contrib import admin
from .models import Post, Like, Comentario

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comentario)