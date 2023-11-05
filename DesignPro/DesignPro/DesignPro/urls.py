from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', include('design.urls')),
]
