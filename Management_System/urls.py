from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/token/', obtain_auth_token, name='api_token'),

    path('task_api/', include('tasks.urls')),
    path('login_api/', include('user.urls')),

]
