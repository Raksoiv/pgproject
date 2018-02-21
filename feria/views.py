from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import feria.models as models


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
    return render(request, 'feria/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def index(request):
    return render(request, 'feria/index.html', {'dashboard': 'active'})


@login_required
def board(request):
    team = request.user.team_set.all()[0]
    tasks = models.Task.objects.filter(feature__epic__team=team)
    backlog = tasks.filter(state=models.Task.BACKLOG)
    in_progress = tasks.filter(state=models.Task.ONGOING)
    done = tasks.filter(state=models.Task.DONE)
    finished = tasks.filter(state=models.Task.ACEPTED)
    return render(
        request,
        'feria/board.html',
        {
            'backlog': backlog,
            'in_progress': in_progress,
            'done': done,
            'finished': finished,
            'board': 'active',
        })
