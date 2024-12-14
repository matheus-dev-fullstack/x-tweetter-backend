from rest_framework import serializers
from usuarios.models import Usuario
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['date_joined', 'name', 'username', 'about', 'photo', 'banner']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  
    class Meta:
        model = Usuario
        fields = [ 'id','name', 'username',  'password', 'photo', 'banner']
    
    def create(self, validated_data):
        try:
            password = validated_data.pop('password', None)
            
            if password:
                validated_data['password'] = make_password(password)

            perfil = super().create(validated_data)
            
            if isinstance(validated_data.get('photo'), InMemoryUploadedFile):
                self._resize_image(perfil.photo.path, (700, 700))

            if isinstance(validated_data.get('banner'), InMemoryUploadedFile):
                self._resize_image(perfil.banner.path, (600, 200))

            return perfil
        except serializers.ValidationError as e:
            print(f"Erro no serializer: {e.detail}")  # Log detalhado no console
            raise e
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")  # Log de erros gerais
            raise serializers.ValidationError({'detail': 'Erro ao criar o usuário.'})
        
    @staticmethod
    def _resize_image(image_path, max_size):
        """Função para redimensionar a imagem"""
        from PIL import Image
        img = Image.open(image_path)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path)
        


    
class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        return token
    
    # def validate(self, attrs):
    #     username = attrs.get('username')
    #     password = attrs.get('password')
        
    #     try:
    #         user = Usuario.objects.get(username=username)
    #     except Usuario.DoesNotExist:
    #         raise serializers.ValidationError("Credenciais inválidas cara.")
        
    #     if not user.check_password(password):
    #         raise serializers.ValidationError("Credenciais inválidas cara.")
        
    #     attrs['user'] = user
    #     return super().validate(attrs)
    
    
    # class LoginSerializer(serializers.Serializer):
    # username = serializers.CharField()
    # password = serializers.CharField()

    # def validate(self, data):
    #     try:
    #         user = Usuario.objects.get(username=data['username'])
    #     except Usuario.DoesNotExist:
    #         raise serializers.ValidationError("Usuário não existe cara.")

    #     if not user.check_password(data['password']): 
    #         raise serializers.ValidationError("Credenciais inválidas cara.")
        
    #     return user