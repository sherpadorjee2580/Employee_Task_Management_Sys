from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def manager_required(view_func):
    """
    Allows access only to logged-in users who are either:
    - Django superusers, or
    - Users whose Profile.role == 'admin'
    Everyone else gets a 403 Forbidden.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        is_manager = request.user.is_superuser or (profile and profile.role == 'admin')
        if not is_manager:
            raise PermissionDenied("You must be a manager/admin to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view