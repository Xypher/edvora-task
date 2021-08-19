from django.urls import path
from .views import change_password_endpoint, delete_session, login_endpoint, signup_endpoint, is_authenticated

urlpatterns = [
    path('signup/', signup_endpoint, name='signup'),
    path('login/', login_endpoint, name='login'),
    path('is_authenticated/', is_authenticated, name="is_authenticated"),
    path('change_password/', change_password_endpoint, name='change_password'),
    path('delete_session/', delete_session, name='delete_session') 
]