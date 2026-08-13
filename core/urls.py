from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='employee/dashboard/', permanent=False)),
    path('employee/', include('Employee_Task_ToDo.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # or whatever this line currently is
]