import typing
from django.http import HttpRequest
from django.shortcuts import redirect

def require_role(role):
    def decorator(view_fn):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.is_anonymous:
                return redirect('main:landing')

            user: typing.Any = request.user
            if user.role != role:
                return redirect('accounts:home')

            response = view_fn(request, *args, **kwargs)
            return response
        return wrapper
    return decorator
