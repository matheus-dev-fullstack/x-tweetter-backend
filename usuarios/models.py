from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Create your models here.
class Usuario(AbstractUser):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    isVerified = models.BooleanField(default=False)
    about = models.TextField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='perfilPhoto', blank=True, null=True)
    banner = models.ImageField(upload_to='bannerPhoto', blank=True, null=True)
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='following',
        blank=True
    )
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # Verifica se já é um hash
            self.password = make_password(self.password)  # Gera o hash da senha
        super().save(*args, **kwargs)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f'{self.name} - {self.username}'
