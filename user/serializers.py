from rest_framework import serializers
from tasks.models import Task



# from tasks.serializers import BookSerializer
from .models import AdminUser, User

class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    role = serializers.CharField()
    
    def create(self, validated_data):
        if validated_data.get('role') == "Admin":
            print("Admin User ")
            return AdminUser.objects.create(**validated_data)
        return User.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = [
            "username",
        ]

class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = [
            "username",
            "email",
          
        ]


class UserSerializer(serializers.Serializer):

    class Meta:
        model = AdminUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "role",

        ]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "role",
        ]

    def update(self, user, validated_data):
        user.username= validated_data.get('username', user.username)
        user.first_name= validated_data.get('first_name', user.first_name)
        user.last_name= validated_data.get('last_name', user.last_name)
        user.email= validated_data.get('email', user.email)
        user.is_active= validated_data.get('is_active', user.is_active)
        user.role= validated_data.get('role', user.role)
        user.save()
        return user



