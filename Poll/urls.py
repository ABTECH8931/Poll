from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Poll_App/', include('Poll_App.urls')),
    path('', include('Poll_App.urls')),
]
