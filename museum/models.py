from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
"""
class Post(models.Model):           # ciascun campo è una colonna della tabella del db
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)    #no parentesi del now
    # per cambiare formato di date_posted, modificare nel template con date_posted | date:"formato che te pare"
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
"""


class Visitor(models.Model):
    number = models.IntegerField(null=False, primary_key=True)
    group = models.IntegerField(null=False)
    date = models.CharField(max_length=50)              # PROBLEM: la data è disponibile solo per pochi log, ovvero quelli che stanno nell' xml
    startTime = models.TimeField(auto_now=False)
    endTime = models.TimeField(auto_now=False)
    presentations = models.IntegerField()
    interruptions = models.IntegerField()

    def __str__(self):
        return str(self.number)

class Event(models.Model):
    visitor_id = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    when = models.TimeField(auto_now=False)
    name = models.CharField(max_length=300)


class Presentation(models.Model):
    visitor_id = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    startTime = models.TimeField(auto_now=False)
    endTime = models.TimeField(auto_now=False)
    name = models.CharField(max_length=200)
    #interrupt = models.IntegerField()

    # TODO remove interrupt


class PointOfInterest(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)
    room = models.IntegerField(null=True)
    backName = models.CharField(max_length=100, null=True)

    # def __str__(self):
    # return self.name


class Position(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    visitor_id = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    poi_id = models.ForeignKey(PointOfInterest, on_delete=models.DO_NOTHING)    #on delete??


