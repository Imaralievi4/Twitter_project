from django.urls import path 
from django.contrib.auth.views import LogoutView

from .views import RegisterView, SigninView


urlpatterns = [
    path('signup/', RegisterView.as_view(), name='sign-up'),
    path('login/', SigninView.as_view(), name='log-in'),
    path('logout/', LogoutView.as_view(), name='log-out'),
]