from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def role_required(required_role: str):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(inst , request, *args, **kwargs):
            if request.user.role == required_role:
                return view_func(inst, request, *args, **kwargs)
            else:
                return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        return wrapper
    return decorator
 