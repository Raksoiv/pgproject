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
        else:
            return render(
                request,
                'feria/login.html',
                {'error': 'Nombre de Usuario o contraseña incorrectos'})
    return render(request, 'feria/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def index(request):
    return render(request, 'feria/index.html', {'dashboard': 'active'})


@login_required
def board(request):
    if request.method == 'POST':
        feature_id = request.POST.get('feature_id')
        feature = models.Feature.objects.get(pk=feature_id)
        name = request.POST.get('name')
        description = request.POST.get('description')
        if request.POST.get('task_id'):
            pk = request.POST.get('task_id')
            state = request.POST.get('state')
            models.Task.objects.filter(id=pk).update(
                feature=feature,
                name=name,
                description=description,
                state=state)
        else:
            new_task = models.Task(
                feature=feature,
                name=name,
                description=description,)
            new_task.save()
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


@login_required
def wbs(request):
    if request.method == 'POST':
        if request.POST.get('epic'):
            team = request.user.team_set.all()[0]
            name = request.POST.get('name')
            description = request.POST.get('description')
            if request.POST.get('epic_id'):
                pk = request.POST.get('epic_id')
                models.Epic.filter(id=pk).update(
                    team=team,
                    name=name,
                    description=description)
            else:
                new_epic = models.Epic(
                    team=team,
                    name=name,
                    description=description)
                new_epic.save()
        if request.POST.get('feature'):
            epic_id = request.POST.get('epic_id')
            epic = models.Epic.objects.get(pk=epic_id)
            name = request.POST.get('name')
            description = request.POST.get('description')
            if request.POST.get('feature_id'):
                pk = request.POST.get('feature_id')
                models.Feature.objects.filter(id=pk).update(
                    epic=epic,
                    name=name,
                    description=description)
            else:
                new_feature = models.Feature(
                    epic=epic,
                    name=name,
                    description=description)
                new_feature.save()
    epics = models.Epic.objects.filter(
        team=request.user.team_set.all()[0])

    return render(request, 'feria/wbs.html', {
        'wbs': 'active',
        'epics': epics
        })


def forum(request):
    return render(request, 'feria/forum.html', {
        'forum': 'active',
        'forums': request.user.team_set.all()[0].forum})


def archivos(request):
    return render(request, 'feria/filesystem.html', {'filesystem': 'active'})
