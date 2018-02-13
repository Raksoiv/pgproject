from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    return render(request, 'feria/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect(request.GET.get('next', '/'))
    elif request.method == 'GET':
        render(request, 'feria/login.html')


def logout_view(request):
    logout(request)
    redirect('/login/')
