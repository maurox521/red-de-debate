from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from resumen.models import Debate

def unique_rand():
    while True:
        code = User.objects.make_random_password(length=4)
        alias = "anonimo_"+code
        if not Profile.objects.filter(alias=alias).exists():
            return alias

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    alias = models.CharField(max_length=30, null=False, unique=True, default=unique_rand, error_messages={'unique':"Ya existe un perfil con este Alias"})
    reputation = models.IntegerField(default=0, blank=True)
    img = models.FileField(blank=True, null=True, default="RDdefault.png")


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=instance)

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User)
    id_debate = models.ForeignKey(Debate)
    message = models.CharField(max_length=300, null=False)
    date = models.DateTimeField(default=datetime.now)
    type = models.CharField(max_length=50, null=False, default="position")
    state = models.IntegerField(default=0)
    def __unicode__(self): # __unicode__ on Python 2
		return self.message

class List(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    owner = models.ForeignKey(User)

class UsersList(models.Model):
    id = models.AutoField(primary_key=True)
    list = models.ForeignKey(List)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=50, default='username')
    def __unicode__(self): # __unicode__ on Python 2
        return self.user.username
