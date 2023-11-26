from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    # decorator
    def decorator(view_func):
        # wrapper function
        def wrapper_func(request, *args, **kwargs):
            print('role', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("<h1>You are not authorized to view this page</h1>")
            
        return wrapper_func
    return decorator