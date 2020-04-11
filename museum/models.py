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
"""         non serve modellare il log??
class Log(models.Model):
    title = models.CharField(max_length=100)
    content_positions = models.TextField()
    content_presentations = models.TextField()
    content_events = models.TextField()
"""

class Group(models.Model):
    number = models.IntegerField(primary_key=True, null=False)
    size = models.IntegerField()
    date = models.CharField(max_length=50)

    def __str__(self):
        return self.number


class Visitor(models.Model):
    number = models.IntegerField(null=False)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    startTime = models.CharField(max_length=30)
    endTime = models.CharField(max_length=30)
    blind = models.CharField(max_length=50)
    headPhones = models.BooleanField()
    notes = models.TextField()
    defect = models.TextField()

    def __str__(self):
        return self.number


class Location(models.Model):
    name = models.CharField(max_length=100, null=False)
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)
    tipo = models.CharField(max_length=100, null=True)
    room = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height= models.IntegerField(null=True)
    backName = models.CharField(max_length=100, null=True)
    #position_x =models.IntegerField()           # inutile??
    #position_y =models.IntegerField()           # inutile??

    def __str__(self):
        return self.name



