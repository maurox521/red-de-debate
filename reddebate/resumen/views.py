# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.views.generic import DetailView, ListView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from resumen.models import Debate
from debate.models import Position, Argument, Counterargument, Rate, PrivateMembers, Visit, newNotification
from perfil.models import Profile, Notification, List, UsersList
from resumen.forms import newDebateForm, LoginForm, orderDebate, orderUser, imageDebate
from taggit.models import Tag
from django.db.models import Q, Sum
from debate.views import updateReputation

def home(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    debate = 'none'
    if next_url:
        meta = next_url.split('/')
        if meta[1]=="debate":
            debate = Debate.objects.get(pk=int(meta[2]))
    if request.user.is_authenticated:
        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return redirect('index')
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('index')
    context = {'form':form, 'debate':debate}
    return render(request,"home.html", context)

def superuser(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('index')
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('index')
    context = {'form':form}
    return render(request,"superuser.html", context)

@login_required
def logout(request):
    django_logout(request)
    return redirect('home')

def closedIndex(request):
    actual_user = request.user
    creator=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',Profile.objects.get(user= request.user).alias)]
    total_users = User.objects.exclude(id=actual_user.id)
    all_users = allUsers(total_users)
    actual_user_list = List.objects.filter(owner_id=actual_user.id).values()
    form = newDebateForm(owner=creator, usuarios=all_users, listado=actual_user_list)
    if request.method == 'GET':
        if 'q' in request.GET:
            deb = search(request)
            public_deb = 0
            private_deb = 0
            for d in deb:
                if(d.members_type == 0): public_deb+=1
                if(d.members_type == 1): private_deb+=1
            debates = debateData(deb, actual_user, False)
            label = "Resultados de la búsqueda: "+str(request.GET.get('q'))
            context = {'total_data_deb': debates, 'actual_user': actual_user, 'alias': Profile.objects.get(user_id= actual_user.id).alias,
                        'form':form, 'label':label,
                        'public_deb': public_deb, 'private_deb': private_deb}
            return render(request, "filtro.html" , context)
    context = makeData(request, actual_user, form, 'closed')
    return render(request, "index.html", context)

##@brief Funcion que showDebate todos los debates
##@param request solicitud web
##@return render redirecciona a "index.html" con la list de todos los debates
##@warning Login is required
@login_required
def index(request):
    actual_user = request.user
    creator=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',Profile.objects.get(user= request.user).alias)]
    total_users = User.objects.exclude(id=actual_user.id)
    all_users = allUsers(total_users)
    actual_user_list = List.objects.filter(owner_id=actual_user.id).values()
    form = newDebateForm(owner=creator, usuarios=all_users, listado=actual_user_list)
    if request.method == 'POST':
        if 'id_deb' in request.POST:
            closeDebate(request)
            return redirect('index')

        if 'id_delete_deb' in request.POST:
            deleteDebate(request)
            return redirect('index')

        if 'id_user_delete' in request.POST:
            id_user = request.POST['id_user_delete']
            user = User.objects.get(pk=id_user)
            user.delete()
            return redirect('index')

        if 'new_img_deb' in request.POST:
            form = imageDebate(request.POST, request.FILES)
            if form.is_valid():
                id = request.POST['deb_img']
                post = Debate.objects.get(pk=id)
                post.img = form.cleaned_data['img']
                post.save()
                return redirect('index')
    if request.method == 'GET':
        if 'q' in request.GET:
            deb = search(request)
            public_deb = 0
            private_deb = 0
            for d in deb:
                if(d.members_type == 0): public_deb+=1
                if(d.members_type == 1): private_deb+=1
            debates = debateData(deb, actual_user, False)
            moderator_view_deb = debateData(deb, actual_user, True)
            label = "Resultados de la búsqueda: "+str(request.GET.get('q'))
            context = {'total_data_deb': debates, 'actual_user': actual_user, 'alias': Profile.objects.get(user_id= actual_user.id).alias,
                        'form':form,'label':label,
                        'deb_pub': public_deb, 'deb_pri': private_deb,
                        'moderator_view_deb':moderator_view_deb}
            return render(request, "filtro.html" , context)
        if 'order' in request.GET:
            order_by = int(request.GET['order'])
            if order_by == 0:
                return JsonResponse(all_users, safe=False)
            elif order_by==1:
                newlist = sorted(all_users, key=lambda k: k['reputation'],reverse=True)
                return JsonResponse(newlist, safe=False)


    context = makeData(request, actual_user, form, 'open')
    return render(request, 'index.html', context)

def makeData(request, actual_user, form, state):
    total_debates = Debate.objects.all().order_by('-id_debate')
    total_data_deb = []
    debates_order = 0
    #cierra debates expirados
    for debate in total_debates:
        ahora = datetime.date.today()
        if debate.state != 'closed' and debate.end_date!= None and debate.end_date <= ahora :
            debate.state = 'closed'
            debate.save()
    #obtener informacion de los debates dependiendo de su estado
    total_debates = Debate.objects.filter(state=state).order_by('-id_debate')
    total_data_deb = debateData(total_debates,actual_user,False)
    moderator_view_deb = debateData(total_debates,actual_user,True)
    if request.method == 'GET':
        if 'order_type' in request.GET:
            debates_order = int(request.GET['order_type'])
            if debates_order == 0:
                total_data_deb = sorted(total_data_deb, key=lambda k: k['model'].id_debate, reverse=True)
                moderator_view_deb = sorted(moderator_view_deb, key=lambda k: k['model'].id_debate, reverse=True)
            elif debates_order == 1:
                total_data_deb = sorted(total_data_deb, key=lambda k: k['visits'], reverse=True)
                moderator_view_deb = sorted(moderator_view_deb, key=lambda k: k['visits'], reverse=True)
            elif debates_order == 2:
                total_data_deb = sorted(total_data_deb, key=lambda k: k['model'].title, reverse=False)
                moderator_view_deb = sorted(moderator_view_deb, key=lambda k: k['model'].title, reverse=False)
            elif debates_order == 3:
                total_data_deb = sorted(total_data_deb, key=lambda k: k['position_num'], reverse=True)
                moderator_view_deb = sorted(moderator_view_deb, key=lambda k: k['position_num'], reverse=True)

    #debates populares por cantidad de posturas
    top_debates = sorted(total_data_deb, key=lambda k: k['position_num'], reverse=True)[:5]
    moderator_top_debates = sorted(moderator_view_deb, key=lambda k: k['position_num'], reverse=True)[:5]
    #perfil del user actual
    user_profile = Profile.objects.get(user_id= actual_user.id)
    user_alias = user_profile.alias
    #obtener tags de los debates publicos
    tags_list = [tag.name for tag in Tag.objects.all()]
    public_debates = Debate.objects.filter(members_type=0)
    top_tags = Debate.tags.most_common(extra_filters={'debate__in': public_debates})[:5]
    #obtener usuarios populares por reputation
    top_reputation = Profile.objects.all().order_by('-reputation')[:5]
    top_users = []
    for user in top_reputation:
        usr = User.objects.get(id=user.user_id)
        profile = Profile.objects.get(user_id=user.user_id)
        top_users.append({'user':usr, 'profile':profile})
    #obtener debates recientes
    recent_debates = Debate.objects.filter(members_type=0, state=state).order_by('-id_debate')[:5]
    recent_data_deb = debateData(recent_debates,actual_user, False)
    moderator_recent_debates = Debate.objects.all().order_by('-id_debate')[:5]
    moderator_recent_data_deb = debateData(moderator_recent_debates,actual_user, True)
    #obtener listado del user actual
    actual_user_list = List.objects.filter(owner_id=actual_user.id).values()
    order_form = orderDebate()
    order_user_form = orderUser()
    img_form = imageDebate()
    context = {'moderator_view_deb':moderator_view_deb, 'total_data_deb': total_data_deb, 'actual_user': actual_user, 'alias': user_alias,
                'form':form, 'top_tags':top_tags, 'top_deb':top_debates,
                'top_users':top_users, 'recent_data_deb': recent_data_deb, 'moderator_recent_deb': moderator_recent_data_deb,
                'moderator_top_deb': moderator_top_debates, 'actual_user_list':actual_user_list,
                'order_form':order_form, 'debates_order':debates_order,
                'order_user_form': order_user_form, 'img_form':img_form}
    return context

def debateData(debates, user, moderator):
    debate_list = []
    for debate in debates:
        infavor_position_num = Position.objects.filter(id_debate_id=debate.id_debate, position=1).count()
        against_position_num = Position.objects.filter(id_debate_id=debate.id_debate, position=0).count()
        argument_num = Argument.objects.filter(id_debate_id=debate.id_debate).count()
        position_num = infavor_position_num + against_position_num
        visits = Visit.objects.filter(id_debate=debate).aggregate(Sum('num')).values()[0]
        if not visits: visits=0
    	if (int(position_num)==0):
            against_percent=0
            infavor_percent=0
    	else:
            infavor_percent = (float(infavor_position_num) / float(position_num))*100
            against_percent = (float(against_position_num) / float(position_num))*100
        if debate.members_type == 1 and not moderator and debate.state == 'open':
            try:
                participate = PrivateMembers.objects.get(id_debate_id=debate.id_debate, id_user_id=user.id)
                debate_list.append({"model":debate, "infavor_percent":infavor_percent, "against_percent":against_percent,
                                        "infavor_position_num":infavor_position_num, "against_position_num":against_position_num,
                                        "position_num":position_num, "arg_num":argument_num,
                                        "visits": visits})

            except:
                participate = False
        else:
            debate_list.append({"model":debate, "infavor_percent":infavor_percent, "against_percent":against_percent,
                                    "infavor_position_num":infavor_position_num, "against_position_num":against_position_num,
                                    "position_num":position_num, "arg_num":argument_num,
                                    "visits": visits})
    return debate_list

def tagged(request, slug):
    actual_user = request.user
    user_profile = Profile.objects.get(user_id= actual_user.id)
    total_users = User.objects.exclude(id=actual_user.id)
    all_users = allUsers(total_users)
    creator=[('username', User.objects.get(id=request.user.id).username),
	         ('alias',user_profile.alias)]
    actual_user_list = List.objects.filter(owner_id=actual_user.id).values()
    form = newDebateForm(owner=creator, usuarios=all_users, listado=actual_user_list)
    debate_list = Debate.objects.filter(tags__slug=slug)
    total_data_deb = debateData(debate_list, actual_user, False)
    moderator_view_deb = debateData(debate_list, actual_user, True)
    top_tags = Debate.tags.most_common()[:5]
    label = "Tags relacionados: "+slug
    context = {'total_data_deb':total_data_deb, 'user': actual_user, 'alias': user_profile.alias,
                 'form':form, 'top_tags':top_tags, 'label':label, 'moderator_view_deb':moderator_view_deb}

    return render(request, 'filtro.html', context)

##@brief Funcion que cierra el debate
##@param request solicitud web
##@return redirect redirecciona a la vista "index"
##@warning Login is required
@login_required
def closeDebate(request):
    id_deb = request.POST['id_deb']
    deb = Debate.objects.get(pk=id_deb)
    deb.state = 'closed'
    deb.save()
    return redirect('closedIndex')

##@brief Funcion que elimina un debate
##@param request solicitud web
##@return redirect redirecciona a la vista "perfil"
##@warning Login is required
@login_required
def deleteDebate(request):
    id_deb=request.POST['id_delete_deb']
    debate = Debate.objects.get(pk=id_deb)
    actual_user = request.user
    if actual_user.is_staff==1:
        debate_text = str(debate.title)
        text = '"'+(debate_text[:30] + '..') if len(debate_text) > 75 else debate_text +'"'
        msg = "Tu debate "+text+" ha sido eliminado por no cumplir las reglas de la red"
        newNotification(debate,debate.id_user_id,'delete_arg',msg,msg)
        updateReputation(debate.id_user_id, -8)
    else:
		updateReputation(actual_user.id, -5)
    debate.delete()
    return redirect('debates')

def search(request):
    query = request.GET.get('q')
    results = Debate.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    return results

def allUsers(total_users):
    all_users = []
    for user in total_users:
        if user.is_staff==0:
            profile = Profile.objects.get(user=user)
            all_users.append({'object':{'id':user.id, 'type':'username'}, 'name':user.username, 'reputation':profile.reputation})
    for user in total_users:
        if user.is_staff==0:
            profile = Profile.objects.get(user=user)
            all_users.append({'object':{'id':user.id, 'type':'alias'}, 'name':profile.alias, 'reputation':profile.reputation})
    return sorted(all_users)

@login_required
def searchView(request):
    actual_user = request.user
    context = makeData(request, actual_user, None, 'open')
    return render(request, "search.html", context)
