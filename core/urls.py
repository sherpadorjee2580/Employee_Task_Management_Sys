from django.contrib import admin
from django.urls import path, include, reverse_lazy

from django.views.generic import RedirectView


urlpatterns = [

    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('', include('Employee_Task_ToDo.manager_urls')),
    path("accounts/", include("accounts.urls")),
      path('', RedirectView.as_view(url=reverse_lazy("employee:dashboard"),permanent=False)),
    path('employee/', include('Employee_Task_ToDo.urls')),
    path('manager/',include('Employee_Task_ToDo.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),  # or whatever this line currently is
    
]
