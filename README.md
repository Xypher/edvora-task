The project should be ready

it has the following endpoints 

-users/signup/ to create a user
 this takes (username, password1, password2) as parameters with password 2 being confirm password
 
-users/login/ to login to an account and create a session
  this takes (username, password) as parameteres
 
-users/change_password/ to change password and delete all sessions except for the current one
  this takes (new_password) as parameter 
  
-users/delete_session/ to delete a specific session
  this takes (session_key) as parameter and deletes a specific session from the backend
 



