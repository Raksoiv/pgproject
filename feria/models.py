from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    n_type = models.PositiveSmallIntegerField()
    uri = models.CharField(max_length=200)


class Team(models.Model):
    user = models.ManyToManyField(User)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='feria/team/logos/')


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='feria/event/logos/')


class Forum(models.Model):
    team = models.OneToOneField('Team', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Message(models.Model):
    forum = models.ForeignKey('Forum', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()


class Response(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class Epic(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()


class Feature(models.Model):
    epic = models.ForeignKey('Epic', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()


class Task(models.Model):
    feature = models.ForeignKey('Feature', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
