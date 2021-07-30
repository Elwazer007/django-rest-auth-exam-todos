from django.urls import path 
from .views import registration_view , ToDoAPIView , ToDoAPIDetailView    , LoginAPI  
from knox import views as knox_views
app_name = 'auth_exam'
urlpatterns = [
    path('register/' , registration_view , name = 'register') , 
    path('login/' , LoginAPI.as_view() , name = 'login') , 
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout') , 
    path('todos/' , ToDoAPIView.as_view() , name = 'todo-list') , 
    path('todos/<int:id>/' , ToDoAPIDetailView.as_view(), name ='todo-detail')
]
