from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path('login/', views.login_view, name='login'),
                  path('register/', views.register, name='register'),
                  path('logout/', views.logout_view, name='logout'),
                  path('main_page/', views.main_page, name='main_page'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
