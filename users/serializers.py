from rest_framework import serializers
from users.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        print("register serializer validation in proccess")
        username = attrs.get('username', '')
        role = attrs.get('role', '')

        ROLE_OPTIONS = ['CONSUMER', 'MERCHANT', 'BANK', 'ADMIN']

        if not username.isalnum():
            raise serializers.ValidationError('username should be alphanumeric')
        
        if not role in ROLE_OPTIONS:
            raise serializers.ValidationError('Invalid role option')

        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(min_length=1, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh_token':user.tokens()['refresh'],
            'access_token':user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        print("Login serializer validation in proccess")
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user= auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account Disabled, contact admin')
        
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            "email":user.email,
            "username":user.username,
            "tokens": user.tokens
        }