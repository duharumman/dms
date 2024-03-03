from django.urls import path
from .views import LoginView, CreateUserView, UserDetailView, UserListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='users'),
    path('create_user/', CreateUserView.as_view(), name='create_user' ),
    path('update_user/<int:user_id>/', UserDetailView.as_view(),  name='update_user')
]