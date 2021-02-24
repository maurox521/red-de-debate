# -*- coding: utf-8 -*-

from channels import Group
import threading
import random
import json
import logging
import ast
from resumen.models import Debate
from debate.models import Argument, Position, PrivateMembers
from django.contrib.auth.models import User
from perfil.models import Profile, List, UsersList
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

log = logging.getLogger(__name__)

def updateReputation(id_usr, score):
    perfil = Profile.objects.get(user_id=id_usr)
    reputation = perfil.reputation + score
    perfil.reputation = reputation
    perfil.save()

@channel_session_user_from_http
def ws_connect(message):
    # prefix, label, id = message['path'].decode('ascii').strip('/').split('/')
    grupo = message['path'].replace("/","")
    Group(grupo).add(message.reply_channel)
    Group(grupo).send({'accept':True})

@channel_session_user
def ws_receive(message):
    grupo = message['path'].replace("/","")
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if data:
        if set(data.keys()) == set(('title', 'text', 'owner_type', 'length', 'args_max', 'counterargs_max', 'counterargs_type', 'members_type', 'position_max','end_date', 'id_user_id', 'members', 'participation_type','tags')):
            data['id_user_id'] = message.user.id
            members = data['members']
            tags = data['tags']
            del data['tags']
            del data['members']
            m = Debate.objects.create(**data)
            for tag in tags:
                m.tags.add(tag)
            updateReputation(message.user.id, 5)
            if data['members_type']=='1':
                id_list=[]
                for member in members:
                    dict_member = ast.literal_eval(member)
                    id = int(dict_member['id'])
                    type = dict_member['type']
                    user = User.objects.get(id=id)
                    id_list.append(user.id)
                    n = PrivateMembers(id_user_id=user.id, id_debate_id=m.id_debate, type=type)
                    n.save()

                n = PrivateMembers(id_user_id=message.user.id, id_debate_id=m.id_debate, type=m.owner_type)
                n.save()
                id_list = set(id_list) #quito los id repetidos
                id_list_unique = []
                for id in id_list:
                    id_list_unique.append(id)
                Group(grupo).send({'text': json.dumps(n.as_dict(id_list_unique))})

            elif data['members_type']=='2':
                m.members_type = 1
                m.save()
                list_users = UsersList.objects.filter(list_id__in=members).values('user_id','type')
                list=[]
                for list_user in list_users:
                    user = User.objects.get(id=list_user['user_id'])
                    type=list_user['type']
                    list.append(user.id)
                    try:
                        n = PrivateMembers.objects.get(id_user_id=user.id, id_debate_id=m.id_debate, type=type)
                    except:
                        n = PrivateMembers(id_user_id=user.id, id_debate_id=m.id_debate, type=type)
                        n.save()
                print(list)
                n = PrivateMembers(id_user_id=message.user.id, id_debate_id=m.id_debate, type=m.owner_type)
                n.save()
            else:
                Group(grupo).send({'text': json.dumps(m.as_dict())})

        elif set(data.keys()) == set(('text','owner_type','id_debate','position','id_user_id')):
            debate = Debate.objects.get(id_debate=data['id_debate'])
            position = Position.objects.get(id_debate_id=debate.id_debate, id_user_id = message.user.id)
            data['id_user_id'] = message.user.id
            data['position'] = position.position
            data['id_debate'] = debate
            m = Argument.objects.create(**data)
            updateReputation(message.user.id, 3)
            Group(grupo).send({'text': json.dumps(m.as_dict())})

        elif set(data.keys()) == set(('position','id_user','id_debate')):
            debate = Debate.objects.get(id_debate=data['id_debate'])
            data['id_user'] = message.user
            data['id_debate'] = debate
            m = Position.objects.create(**data)
            updateReputation(message.user.id, 3)
            Group(grupo).send({'text': json.dumps(m.as_dict())})


        elif set(data.keys()) == set(('position', 'id_debate', 'razon')):
            debate = Debate.objects.get(id_debate=data['id_debate'])
            data['id_debate'] = debate
            m = Position.objects.get(id_debate_id=debate.id_debate, id_user_id=message.user.id)
            m.position = data['position']
            m.change = data['razon']
            m.count_change = m.count_change + 1
            m.save()
            Group(grupo).send({'text': json.dumps(m.as_dict())})



@channel_session_user
def ws_disconnect(message):
    grupo = message['path'].replace("/","")
    Group(grupo).send({'close':True})
    Group(grupo).discard(message.reply_channel)
