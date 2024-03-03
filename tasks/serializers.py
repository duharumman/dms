from datetime import datetime
from rest_framework import serializers
from user.decorators import role_required
from user.models import User, AdminUser
from tasks.models import Task, Book 
from user.serializers import UserBookSerializer, AdminUserSerializer
from user.models import Role


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=150)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    deadline = serializers.DateTimeField()  
    status = serializers.CharField(max_length=20)
    min_users = serializers.IntegerField()

    def create(self, validated_data):
        return Task.objects.create(**validated_data)



class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book 
        fields = [ 'task', 'users']

    def validate(self, validated_data):
        task = validated_data.get('task')
        users = validated_data.get('users')

        if len(users) > task.min_users :
            raise serializers.ValidationError("Number of users is less than the required minimum.")
        return super().validate(validated_data)
    
    def create(self, validated_data):
        context = self.context
        assigned_by = context.get('user')
        validated_data['assigned_by']= assigned_by
        users = validated_data.get("users")
        task = validated_data.get("task")
        existing_book = Book.objects.filter(task=task).first()

        if existing_book:
            existing_book.users.set(users)
            existing_book.save()
            return  existing_book
        
        return super().create(validated_data)
    
class BookSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    users = UserBookSerializer(many=True)
    assigned_by = AdminUserSerializer()
    class Meta:
        model = Book
        fields = ['task', 'users', 'assigned_by']


class BookUserSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    assigned_by = AdminUserSerializer()
    class Meta:
        model = Book
        fields = ['task', 'assigned_by']
class UpdateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields =[
            'title',
            "description",
            "status",
            "deadline",
            "created_at",
            "updated_at",
        ]
    @role_required(Role.ADMIN)
    def update(self, task, validated_data):
        task.title = validated_data.get('title', task.title)    
        task.description = validated_data.get('description', task.description)
        task.deadline = validated_data.get('deadline', task.deadline)
        task.status = validated_data.get('status', task.status)
        task.updated_at = datetime.now()
        task.save()
        return task
    
    @role_required(Role.USER)
    def update_status(self, task, validated_data):
        task.status = validated_data.get('status', task.status)    
        task.updated_at = datetime.now()
        task.save()
        return task

   

class BatataSerializer(serializers.Serializer):
   
    username =serializers.CharField()
    first_name =serializers.CharField()
    last_name =serializers.CharField()
    email =serializers.EmailField()
    role =serializers.CharField()
    books = BookUserSerializer(many=True)
