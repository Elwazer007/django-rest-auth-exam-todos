from rest_framework import serializers
from auth_exam.models import User ,ToDo
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate  
from datetime import datetime
class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())]) 
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User 
        fields = ['first_name' , 'last_name' , 'username' , 'date_of_birth','email' , 'password' , 'password2'] 
        extra_kwargs = {
				'password': {'write_only': True , 'required' : True}, 
                'username' : {'required' : True}  ,
                'date_of_birth': {'required' : True}  , 
                'first_name' : {'required' : True}  ,
                'last_name' : {'required' : True}  ,
                'password2': {'required' : True}  ,
		}	 


    def save(self):
        user = User(first_name = self.validated_data['first_name'] , last_name = self.validated_data['last_name'], username = self.validated_data['username'] , date_of_birth = self.validated_data['date_of_birth'] , email = self.validated_data['email'] )
        password = self.validated_data['password']
        password2 = self.validated_data['password2'] 
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})  

        curr_date = datetime.now()
        curr_date = datetime.date( curr_date)
        if curr_date < self.validated_data['date_of_birth']:
            raise serializers.ValidationError('Invalid Date')
        if len(password) < 8:
            raise serializers.ValidationError('The password is not strong enough')
        user.set_password(password)
        user.save()
        return user 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username' , 'first_name' , 'last_name' ,'email' , 'date_of_birth')

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        user = authenticate(**data)
        print(user.is_authenticated)
        if user and user.is_active:
            return user 
        raise serializers.ValidationError("Invalid Details.")    


class ToDoDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo 
        exclude = ('user' , ) 
        extra_kwargs = {
                'completed' : {'required' : True}  ,   # i found issue here for the completed boolean to be required , i tried some stack over flow and docs solutions and didn't solve it
                'due' : {'required' : True}  , 
                'title' : {'required' : True} , 
                'description' : {'required' : True} , 
		}	 

    
    """ def save(self):

        todo = ToDo.objects.create(
            user = self.context['user'],
            title=self.validated_data["title"],
            description=self.validated_data["description"],
            completed=self.validated_data["completed"],
            due = self.validated_data["due"] ,
        )
        return todo """

    def create(self, validated_data):
        return ToDo.objects.create(user = self.context['user'] ,title = self.validated_data['title'] , due = self.validated_data['due'], completed = self.validated_data['completed'] , description = self.validated_data['description'])
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.completed = validated_data.get('created', instance.completed)
        instance.due =  validated_data.get('due', instance.due)
        print('------------------------------------------------------------')
        instance.save()
        return instance


    