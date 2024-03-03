import pdb
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import authenticate

from tasks.serializers import BatataSerializer

from .serializers import LoginSerializer, CreateUserSerializer, UpdateUserSerializer,UserSerializer
from .models import User
from .decorators import role_required
from user.models import Role



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)


            if user:
                if user.is_admin:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'role': 'admin'}, status=status.HTTP_200_OK)
                elif user.is_user:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'role': 'user'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
       

class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]

    @role_required(Role.ADMIN)
    def post(self , request):
        serializer = CreateUserSerializer(data=request.data)
        
        if serializer.is_valid:
            serializer = CreateUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

            user = User.objects.get(username=request.data['username'])
            token, created = Token.objects.get_or_create(user=user)
    
            return Response({'token': token.key, 'role': serializer.data['role']}, status=status.HTTP_201_CREATED)
        
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            user =User.objects.select_related('books__users').get(pk=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail':"User not found"}, status=status.HTTP_404_NOT_FOUND)


    @role_required(Role.ADMIN)
    def post(self, request, user_id):
        try:
            user =User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail':"User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateUserSerializer(instance=user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request): 
        users = User.objects.prefetch_related('books__task').all()
        serializer =  BatataSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)