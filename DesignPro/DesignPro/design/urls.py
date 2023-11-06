from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import IndexView, LoginView, RegisterView, LogoutView, MainPageView, ProfileView, CreateRequestView, \
    DeleteRequestView

urlpatterns = [
                  path('', IndexView.as_view(), name='index'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('main_page/', MainPageView.as_view(), name='main_page'),
                  path('profile/', ProfileView.as_view(), name='profile'),
                  path('create_request/', CreateRequestView.as_view(), name='create_request'),
                  path('delete_request/<int:pk>/', DeleteRequestView.as_view(), name='delete_request'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
