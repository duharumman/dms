import pdb
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status

from user.models import Role
from .models import Task, Book
from .serializers import TaskSerializer, UpdateTaskSerializer, CreateBookSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticated
from user.decorators import role_required


class TaskListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    @role_required(Role.ADMIN)
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, task_id):
        try:
            task =Task.objects.get(pk=task_id)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, task_id):
        try:
            task =Task.objects.get(pk=task_id)
            serializer = UpdateTaskSerializer()
            update_method = serializer.update if request.user.role == Role.ADMIN else serializer.update_status

            serializer = UpdateTaskSerializer(instance=task, data=request.data, context={'update_method': update_method})
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CreateBookView(APIView):
    permission_classes = [IsAuthenticated]
    @role_required(Role.ADMIN)
    def post(self, request):
        
        serializer = CreateBookSerializer(data=request.data,context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListBookView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        books =Book.objects.all()
        serializer =  BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
