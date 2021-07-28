from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics

from rest_framework.decorators import api_view 
from knox.models import AuthToken 
from .serializers import CreateUserSerializer  , LoginUserSerializer , UserSerializer


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


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        print(user.date_of_birth)
        return Response({
            "token": AuthToken.objects.create(user)[1] , 
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })



