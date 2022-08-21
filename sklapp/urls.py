from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('sklapp/', include('items.urls')),
    path('admin/', admin.site.urls),
    path('', include('hub.urls')),
]
