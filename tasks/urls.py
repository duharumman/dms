from django.urls import path
from .views import TaskListView, CreateTaskView, TaskDetailsView, CreateBookView, ListBookView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('ceate-task/', CreateTaskView.as_view(), name='create_task'),
    path('task/<int:task_id>/', TaskDetailsView.as_view(), name="task_details"),
    path('booking/', CreateBookView.as_view(), name='book'),
    path('books/', ListBookView.as_view(), name='all_books')
]