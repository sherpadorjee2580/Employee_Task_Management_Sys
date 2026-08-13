from django.contrib import admin
from django.urls import path, include, reverse_lazy

from django.views.generic import RedirectView
from accounts.views import post_login_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('', post_login_redirect, name='home'),
    path('', include('Employee_Task_ToDo.manager_urls')),   # now actually included
    path('employee/', include('Employee_Task_ToDo.urls')),
]
