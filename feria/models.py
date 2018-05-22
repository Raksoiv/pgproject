from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Team(models.Model):
    user = models.ManyToManyField(User)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='feria/team/logos/', null=True)


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='feria/event/logos/', null=True)


class Forum(models.Model):
    team = models.OneToOneField('Team', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    public = models.BooleanField()


class Message(models.Model):
    class Meta:
        ordering = ['-updated_at']

    forum = models.ForeignKey('Forum', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    class Meta:
        ordering = ['-updated_at']

    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Epic(models.Model):
    class Meta:
        ordering = ['id']

    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Feature(models.Model):
    class Meta:
        ordering = ['-updated_at']

    epic = models.ForeignKey('Epic', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    criteria = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    BACKLOG = 0
    ONGOING = 1
    DONE = 2
    ACEPTED = 3
    STATE_CHOICES = (
        (BACKLOG, 'No Iniciada'),
        (ONGOING, 'En Desarrollo'),
        (DONE, 'Terminada'),
        (ACEPTED, 'Aceptada'))

    feature = models.ForeignKey('Feature', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    state = models.PositiveSmallIntegerField(
        choices=STATE_CHOICES,
        default=BACKLOG)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
