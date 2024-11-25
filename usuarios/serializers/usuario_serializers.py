from rest_framework import serializers
from usuarios.models import Usuario
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        # fields = ['id', 'name', 'username']
        # fields = ['id', 'name', 'username', 'perfilPhoto']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Define que o campo password é de escrita, não será retornado na resposta
    class Meta:
        model = Usuario
        # fields = [ 'id','name', 'username', 'perfilPhoto', 'password']
        fields = [ 'id','name', 'username',  'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        username = validated_data['username']

        if Usuario.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists.')
        if password:
            validated_data['password'] = make_password(password)

        return super().create(validated_data)
        

    
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