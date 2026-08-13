from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def manager_required(view_func):
    """
    Allows access only to logged-in users who are either:
    - Django superusers or staff members, or
    - Assigned to the 'Manager' group.
    Everyone else gets a 403 Forbidden.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        is_manager = (
            request.user.is_superuser 
            or request.user.is_staff 
            or request.user.groups.filter(name='Manager').exists()
        )
        if not is_manager:
            raise PermissionDenied("You must be a manager/admin to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view