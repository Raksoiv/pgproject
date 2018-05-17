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
def epics(request):
    if request.method == 'POST':
        e = models.Epic.objects.get(pk=request.POST.get('id'))
        e.name = request.POST.get('name')
        e.description = request.POST.get('description')
        e.save()
    return render(request, 'feria/epics.html', {
        'epics': 'active',
    })


def epic_detail(request, epic_id):
    return render(request, 'feria/epic_detail.html', {
            'e': models.Epic.objects.get(pk=epic_id),
        })


def forum(request):
    return render(
        request,
        'feria/forum.html', {
            'forum': 'active',
            'user_forums':
                list(models.Forum.objects.filter(public=True))
                + list(t.forum for t in request.user.team_set.all())
        })


def forum_detail(request, forum_id):
    f = models.Forum.objects.get(pk=forum_id)
    if request.method == 'POST':
        new_message = models.Message(
            forum=f,
            user=request.user,
            title=request.POST['title'],
            content=request.POST['nessage_text'])
        new_message.save()
    return render(
        request,
        'feria/forum_detail.html', {
            'forum': 'active',
            'f': f,
        })


def message_detail(request, message_id):
    message = models.Message.objects.get(pk=message_id)
    if request.method == 'POST':
        new_answer = models.Answer(
            message=message,
            user=request.user,
            content=request.POST['nessage_text'],
            )
        new_answer.save()
    return render(
        request,
        'feria/message_detail.html', {
            'forum': 'active',
            'm': message,
            'answers': message.answer_set.all().order_by('created_at')
        })


def archivos(request):
    return render(request, 'feria/filesystem.html', {'filesystem': 'active'})
