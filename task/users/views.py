from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.contrib.auth import update_session_auth_hash
from django.http import QueryDict

# Create your views here.

#logs the user in
@csrf_exempt
def login_endpoint(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"status": "successful", "message": "you are logged in"})
    else:
        return JsonResponse({"status": "unsuccessful", "message": "login failed"})
        

#sign in the user
@csrf_exempt
def signup_endpoint(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"status": "failed", "message": form.error_messages})
        form.save()
        return JsonResponse({"status": "successful", "message": "signup is successful"})

#checks if the user is authenticated (aka valid session)
@csrf_exempt
def is_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse({"message": "you are authenticated"})
    else:
        return JsonResponse({"message": "you are not authenticated"})
    
    
#delete a session (it uses a post method not delete as delete not supported by django)
@csrf_exempt
def delete_session(request):
    sessions = Session.objects.get(session_key=request.POST["session_key"]) #gets the session
    sessions.delete()
    return JsonResponse({"message": "session deleted"})    



@csrf_exempt
def change_password_endpoint(request):

    request.user.set_password(request.POST['new_password'])
    request.user.save()

    #recalculate the session hash after a change to the user's password
    update_session_auth_hash(request, request.user)


    session_list = get_sessions(request.user, request.session)
    session_list.delete()

    
    return JsonResponse({
        "messages": "all sessions deleted",
        "username": request.user.username,
        "new_password": request.POST['new_password']
    })

def get_sessions(user, current_session):

    """
    get's all sessions associated with a user except the current session
    """
    user_sessions = []
    all_sessions  = Session.objects.all()
    for session in all_sessions:
        session_data = session.get_decoded()
        if user.pk == int(session_data.get('_auth_user_id')) and session.session_key != current_session.session_key:
            user_sessions.append(session.pk)
    
    return Session.objects.filter(pk__in=user_sessions)


