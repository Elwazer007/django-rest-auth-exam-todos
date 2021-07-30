from django.contrib.auth import login
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics
from datetime import datetime
from auth_exam.models import ToDo , User
from rest_framework.decorators import api_view
from knox.models import AuthToken 
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateUserSerializer  , LoginUserSerializer , UserSerializer , ToDoSerializer , ToDoDetailedSerializer
from rest_framework.pagination import PageNumberPagination

@api_view(['POST', ]) 
def registration_view(request):

    if request.method == 'POST':
        serializer = CreateUserSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save() 
            data['response'] = 'successfully registered new user.'
            token = AuthToken.objects.create(user)[1]

        else:
            data = serializer.errors 
            
        return Response(data)



class ToDoAPIView(APIView):
    permission_classes = [IsAuthenticated , ]
    def post(self , request , format = None):
         serializer = ToDoDetailedSerializer(data=request.data , context = {'user':request.user})
         if serializer.is_valid():
            todo = serializer.save() 
            serializer = ToDoDetailedSerializer(todo)
            return Response(serializer.data , status = status.HTTP_201_CREATED)
         else:
            return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST) 


    def get(self , request , format = None):
        paginator = PageNumberPagination()
        paginator.page_size = 20
        todos = ToDo.objects.filter(user = request.user)
        result_page = paginator.paginate_queryset(todos, request)
        serializer = ToDoSerializer(result_page , many = True)
        start = (request.query_params.get('start'))
        limit = (request.query_params.get('limit'))
        if start is not None and limit is not None:
            start = int(start)
            limit = int(limit)
            todos = ToDo.objects.filter(user = request.user , id__gte = start , id__lte = start + limit - 1)
            result_page = paginator.paginate_queryset(todos, request)
            serializer = ToDoSerializer(result_page , many = True)

        return paginator.get_paginated_response(serializer.data)




class ToDoAPIDetailView(APIView):
    permission_classes = [IsAuthenticated , ]
    def get(self , request , *args , **kwargs):
        todo = get_object_or_404(ToDo , pk = kwargs['id'])
        if todo.user != request.user:
            return Response({'error':"You don't have permission to get this."}) 
        serilizer = ToDoDetailedSerializer(todo)
        return Response(serilizer.data)
    def delete(self, request, *args, **kwargs):
        todo = get_object_or_404(ToDo, pk=kwargs['id'])
        if todo.user != request.user:
            return Response({'error':"You don't have permission to delete this."} , status=status.HTTP_401_UNAUTHORIZED)
        todo.delete()
        return Response("ToDo deleted", status=status.HTTP_204_NO_CONTENT) 

    def put(self , request , *args , **kwargs):
        todo = get_object_or_404(ToDo , pk = kwargs['id'])
        if todo.user != request.user:
            return Response({'error':"You don't have permission to update this."} , status=status.HTTP_401_UNAUTHORIZED)
        serializer = ToDoSerializer(todo, data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self , request , *args , **kwargs):
         todo = get_object_or_404(ToDo , pk = kwargs['id']) 
         if todo.user != request.user:
            return Response({'error':"You don't have permission to update this."}) 
         serializer = ToDoSerializer(todo, data=request.data,  partial=True)
         if serializer.is_valid():
            todo = serializer.save()
            return Response(ToDoSerializer(todo).data)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data 
        login(request, user)
        print("curr user" , user)
        return Response({
            "token": AuthToken.objects.create(user)[1] , 
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        }) 

class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,
                          ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

