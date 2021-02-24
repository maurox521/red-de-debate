# coding=utf-8
from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required
import ast
import re

from django.http import HttpResponse
from django.shortcuts import redirect
import requests
from collections import Counter
import math
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from resumen.models import Debate
from perfil.models import Profile, List, UsersList
from debate.models import Position, Argument, Counterargument, Report, Visit
from perfil.forms import updateAlias, newList, selectUsers, selectList, updateImage
from resumen.views import debateData, closeDebate, allUsers
from debate.views import updateReputation

##@brief Funcion que showDebate los datos del user, debates abiertos, closedIndex y opciones para cada uno.
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def username(request, id_usr):
    user_data = userData(request,id_usr,'username')
    return user_data

def alias(request, alias):
    id_usr = Profile.objects.get(alias=alias).user_id
    user_data = userData(request,id_usr,'alias')
    return user_data

def userData(request,id_usr,name_type):
    try:
        target_user = User.objects.get(id=id_usr)
    except ObjectDoesNotExist:
        return render(request, '404.html', status=404)
    target_profile = Profile.objects.get(user_id=target_user)
    actual_user = request.user
    #si el user actual accede a su propio perfil
    if actual_user.id==target_user.id:
        alias_form = updateAlias(instance=target_profile)
        imagen_form = updateImage()
        if request.method == 'POST':
            #solicitud de cambiar alias
            if 'new_alias' in request.POST:
                alias_form = updateAlias(request.POST, instance=target_profile)
                if alias_form.is_valid():
                    post = alias_form.save(commit=False)
                    alias =  request.POST['alias']
                    alias = re.sub('[^A-Za-z0-9]+', '', alias)
                    post.alias = alias
                    post.save()
                    return redirect('username',id_usr=actual_user.id)
            #solicitud de cambiar imagen de perfil
            elif 'new_image' in request.POST:
                form = updateImage(request.POST, request.FILES)
                if form.is_valid():
                    post = Profile.objects.get(user=actual_user)
                    post.img = form.cleaned_data['img']
                    post.save()
                    return redirect('username',id_usr=actual_user.id)
        stats = userStats(actual_user.id)
        reports = Report.objects.all()
        data_report = []
        for report in reports:
            if int(report.reason)==0:
                reason = "Lenguaje"
            elif int(report.reason)==1:
                reason = "Privacidad"
            elif int(report.reason)==2:
                reason = "Publicidad"
            if report.type=='debate':
                element=Debate.objects.get(pk=report.debate_id)
            elif report.type=='argument':
                element=Argument.objects.get(pk=report.argument_id)
            elif report.type=='counterarg':
                element=Counterargument.objects.get(pk=report.counterarg_id)
            reported= element.id_user
            owner = User.objects.get(pk=report.owner_id)
            data_report.append({'reason':reason, 'type':report.type ,'element':element,
                                'reported':reported, 'owner':owner})
        return render(request, 'perfil_usuario.html', {'actual_user': actual_user,
            'alias': target_profile, 'alias_form': alias_form,
            'stats': stats, 'imagen_form':imagen_form, 'data_report':data_report})
    #si el user accede al perfil de otro user
    else:
        stats = userStats(target_user.id)
        target_user_list = UsersList.objects.filter(user_id = target_user.id, type=name_type)
        actual_user_list = List.objects.filter(owner_id=actual_user.id)
        available_list = actual_user_list.exclude(id__in=target_user_list.values('list_id')).values()
        already_in_list = actual_user_list.filter(id__in=target_user_list.values('list_id')).values()
        total_users = User.objects.all()
        all_users = allUsers(total_users)
        form = selectList(listas=available_list, user=target_user.id)
        form_list = newList(actual_user=request.user.id)
        if request.method == 'POST':
            #solicitud de agregar user a una list existente
            if 'new_user_list' in request.POST:
                usr = request.POST['user']
                type = request.POST['type_user']
                select = request.POST.getlist('list_id')
                if (len(select)>0):
                    for list in select:
                        post = UsersList(user_id=usr, list_id=list, type=type)
                        post.save()
                    return redirect('username', id_usr=usr)
                else:
                    return redirect('username', id_usr=usr)
            #solicitud de agregar user a una list nueva
            if request.POST['name']:
                usr = request.POST['user']
                type = request.POST['type_user']
                form_list = newList(request.POST,actual_user=request.user.id)
                if form_list.is_valid():
                    list = form_list.save(commit=False)
                    list.owner = request.user
                    list.save()
                    new_usr = UsersList(user_id=usr, list_id=list.id, type=type)
                    new_usr.save()
                    return redirect('username', id_usr=usr)
        return render(request, 'perfiles.html', {'target_user': target_user,
            'alias': target_profile, 'name_type': name_type,
            'stats': stats, 'form':form, 'form_list':form_list,
            'already_in_list':already_in_list, 'all_users':all_users})

#estadisticas de un user
def userStats(id_user):
    total_debates = Debate.objects.all().order_by('-id_debate')
    user_debates = Debate.objects.filter(id_user_id= id_user)
    user_participation = Position.objects.filter(id_user_id=id_user).values('id_debate_id')
    user_participation_deb = Debate.objects.filter(id_debate__in=user_participation)
    user_tags = findUserTags(user_debates, user_participation_deb)
    user_deb_num = Debate.objects.filter(id_user_id= id_user).count()
    user_position_num = Position.objects.filter(id_user_id = id_user).count()
    user_args_num = Argument.objects.filter(id_user_id = id_user).count()
    user_counterargs_num = Counterargument.objects.filter(id_user_id = id_user).count()
    reached_users = Visit.objects.filter(id_debate__in=user_debates).count()
    best_arg = 0
    worse_arg = 0
    for debate in total_debates:
        try:
            user_position = Position.objects.get(id_debate_id=debate.id_debate, id_user_id=id_user).position
        except:
            user_position = "vacia"
        if (debate.state == "cerrado"):
            infavor_position_num = Position.objects.filter(id_debate_id=debate.id_debate, position=1).count()
            against_position_num = Position.objects.filter(id_debate_id=debate.id_debate, position=0).count()
            arguments = Argument.objects.filter(id_debate_id=debate.id_debate).order_by('-score')

            if len(arguments)!=0:
                best_argument = arguments[0]
                worse_argument = arguments[len(arguments)-1]
                if best_argument.id_user.id == id_user:
                    best_arg += 1
                if worse_argument.id_user.id == id_user:
                    worse_arg += 1

    stats = {'deb_num': user_deb_num, 'position_num':user_position_num,
             'args_num': user_args_num, 'counterargs_num':user_counterargs_num,
             'best_arg':best_arg, 'worse_arg':worse_arg,
             'tags':user_tags, 'reached_users':reached_users}
    return stats

#debates de un user
def userDebates(request):
    if request.method == 'POST':
        #solicitud de cerrar un debate
        if 'id_deb' in request.POST:
            closeDebate(request)
            return redirect('debates')
        #solicitud de eliminar un debate
        if 'id_delete_deb' in request.POST:
            deleteDebate(request)
        #solicitud de republicar un debate
        if 'id_deb_republish' in request.POST:
            republishDebate(request)
    actual_user = request.user
    actual_user_debates = Debate.objects.filter(id_user_id= actual_user.id).order_by('-id_debate')
    total_data_deb = debateData(actual_user_debates,actual_user,False)
    return render(request, 'debates_usuario.html', {'actual_user': actual_user, 'total_data_deb': total_data_deb})

def findUserTags(debate, participations):
    tags_usr = []
    for deb in debate:
        tags = deb.tags.all().values()
        for tag in tags:
            tags_usr.append(tag['slug'])
    for deb in participations:
        tags = deb.tags.all().values()
        for tag in tags:
            tags_usr.append(tag['slug'])
    tags_dict = dict(Counter(tags_usr))
    keys = [item.strip() for item in tags_dict.keys()]
    size = tags_dict.values()
    norm_size = [float(i)/max(size) * 10 for i in size]
    norm_size = [int(math.ceil(i)) for i in norm_size]
    dictionary = dict(zip(keys,norm_size))
    return dictionary

#se despliegan  todas las listas del user
def userList(request):
    actual_user_list = List.objects.filter(owner=request.user).values()
    users_in_list = []
    for item in actual_user_list:
        usr_list = UsersList.objects.filter(list_id=item['id']).values()
        for user in usr_list:
            username = User.objects.get(id=user['user_id'])
            profile = Profile.objects.get(user_id=user['user_id'])
            users_in_list.append({'name':username, 'list_id':user['list_id'],
                                  'alias':profile.alias, 'type':user['type']})
    form_list = newList(actual_user=request.user.id)
    if request.method == 'POST':
        #solicitud de crear una nueva lista
        if 'name' in request.POST:
            form_list = newList(request.POST, actual_user=request.user.id)
            if form_list.is_valid():
                list = form_list.save(commit=False)
                list.owner = request.user
                list.save()
                return redirect('memberList', list.id)
        #solicitud de eliminar una list
        if 'id_list' in request.POST:
            id_list = request.POST['id_list']
            user_list = List.objects.get(id=id_list)
            user_list.delete()
            return redirect('userList')

    return render(request, 'listas_usuario.html', {'actual_user':request.user, 'actual_user_list': actual_user_list, 'form_list': form_list,
                'users_in_list': users_in_list})
#se despliegan los miembros de cada list
def memberList(request, id_list):
    try:
        list = List.objects.get(id=id_list)
    except ObjectDoesNotExist:
        return render(request, '404.html', status=404)
    list_users = UsersList.objects.filter(list_id=id_list)
    list_profile = []
    for user in list_users:
        profile = Profile.objects.get(user_id=user.user_id)
        list_profile.append({'user':user, 'perfil':profile, 'type':user.type})
    exclude = [request.user.id]
    for item in list_users:
        exclude.append(item.user_id)
    total_users = User.objects.exclude(id__in=exclude)
    all_users = allUsers(total_users)
    usrlist_form = selectUsers(usuarios=all_users, list=id_list)

    if request.method == 'POST':
        #solicitud de agregar usuarios a una list
        if 'user' in request.POST:
            select = request.POST.getlist('user')
            for usr in select:
                dict_usr = ast.literal_eval(usr)
                id=dict_usr['id']
                type=dict_usr['type']
                post = UsersList(user_id=id, list_id=request.POST['list_id'], type=type)
                post.save()
            return redirect('memberList', request.POST['list_id'])
        #solicitud de eliminar usuarios de una list
        if 'id_usr_lista' in request.POST:
            id_usr = request.POST['id_usr_lista']
            id_list = request.POST['id_list']
            type = request.POST['type_user']
            user_list = UsersList.objects.get(list_id=id_list, user_id=id_usr, type=type)
            user_list.delete()
            return redirect('memberList', id_list)
    return render(request, 'lista.html', {'list': list, 'list_profile': list_profile, 'form': usrlist_form})

##@brief Funcion que actualiza el debate "cerrado" a "abierto"
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def republishDebate(request):
    id_deb=request.POST['id_deb_republish']
    opc=request.POST['tab']
    deb = Debate.objects.get(pk=id_deb)
    if opc == "deleteDebClosed":
        deb.delete()
    else:
        if opc == "NULL":
            deb.end_date = None
        elif opc=="fechafin":
            yyyy,mm,dd=str(request.POST['nuevafecha']).split("-")
            deb.end_date = datetime.date(int(yyyy),int(mm),int(dd))
        deb.state = 'open'
        deb.save()
    return redirect('debates')

def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
