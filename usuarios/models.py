from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

# Create your models here.
class Usuario(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    isVerified = models.BooleanField(default=False)
    about = models.TextField(max_length=200, blank=True)
    perfilPhoto = models.ImageField(upload_to='perfilPhoto', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # Verifica se já é um hash
            self.password = make_password(self.password)  # Gera o hash da senha
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.name} - {self.username}'
