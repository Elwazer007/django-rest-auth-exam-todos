# django-rest-auth-exam-todos
Todo rest api implemented with django-rest-framework and used django-rest-knox for authentication 
to run this project  go to master branch and just clone it and run 'poetry install' (which is used to manage the dependencies) register as a new user ,  login and have your token  and use Postman or any related service to test it !.

Currently i provide these different endpoints for requests : 
1 - Get to-dos (​GET /todos/​) -- this gets all todos owned
2 - Get one to-do (​GET /todos/<int:id>/​) gets a specific todo owned by the user 
3 - Create a new to-do (​POST /todos/​) 
4 - Update a to-do (​PUT /todos/<int:id>/​) 
5 - Partially update a to-do (​PATCH /todos/<int:id>/​)  
6 - Delete a to-do (​DELETE /todos/<int:id>/​)

