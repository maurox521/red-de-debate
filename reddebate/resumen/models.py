# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from datetime import *
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
import unicodedata

# Create your models here.
class Debate(models.Model):
    #parametros de la tabla.
    id_debate = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateField(default=datetime.now, blank=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    owner_type = models.CharField(max_length=50, default='username')
    length = models.IntegerField(default=300, blank=True)
    id_user = models.ForeignKey(User)
    state = models.CharField(max_length=20, default='open')
    args_max = models.IntegerField(default=1)
    position_max = models.IntegerField(default=3)
    counterargs_max = models.IntegerField(default=1)
    counterargs_type = models.IntegerField(default=0) # 0:ambas # 1: contraria
    members_type = models.IntegerField(default=0) #0 debate publico
    participation_type = models.CharField(max_length=50, default='all')
    img = models.FileField(blank=True, null=True, default="RDdefault.png")

    tags = TaggableManager()

    def __unicode__(self): # __unicode__ on Python 2
		return self.title
    def __getitem__(self, key):
        return getattr(self, key)
    def as_dict(self):
        return {'text': self.text, 'type':self.members_type, 'id':self.id_debate}
