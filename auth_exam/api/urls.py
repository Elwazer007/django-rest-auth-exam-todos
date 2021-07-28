from django.urls import path 
from .views import registration_view  , LoginAPI
from knox import views as knox_views

urlpatterns = [
    path('register/' , registration_view , name = 'register') , 
    path('login/' , LoginAPI.as_view() , name = 'login') , 
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout')
]
