# coding=utf-8
from django.shortcuts import render, redirect

from resumen.models import Debate
from debate.models import Position, Argument, Rate, Counterargument, PrivateMembers, Visit, Report,newNotification
from perfil.models import Profile, Notification
from debate.forms import newArgForm1,newArgForm0, newCounterargForm, newReportReasonForm, updateImage


from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from datetime import *
import itertools
import json
import datetime
import pytz

##@brief Funcion que showDebate el debate
##@param request solicitud web
##@param id_debate id del debate solicitado por la url dinamica
##@return render redirecciona a "Debate" si el debate esta abierto y "debate_cerrado" si no
##@warning Login is required
@login_required
def showDebate(request, id_debate): #debate_id
	try:
		debate = Debate.objects.get(id_debate= id_debate)
	except ObjectDoesNotExist:
		return render(request, '404.html', status=404)
	visits = visitCount(debate, request.user)
	if request.method == 'POST':
		#solicitud de publicar un argumento a favor
		if 'textArg1' in request.POST:
			arg = newArgument(request, id_debate, 1)
			return redirect(showDebate,id_debate)
		#solicitud de publicar un argumento en contra
		if 'textArg0' in request.POST:
			arg = newArgument(request, id_debate, 0)
			return redirect(showDebate,id_debate)
		#solicitud de valorar un argumento
		if 'id_arg' in request.POST:
			respuesta = rateArgument(request)
			return HttpResponse(respuesta)
		#solicitud de publicar un contraargumento a favor
		if 'counterargument0' in request.POST:
			counterarg = newCounterargument(request, id_debate, "id_argument0")
			return redirect(showDebate,id_debate)
		#solicitud de publicar un contraargumento en contra
		if 'counterargument1' in request.POST:
			counterarg = newCounterargument(request, id_debate, "id_argument1")
			return redirect(showDebate,id_debate)
		#solicitud de eliminar un argumento
		if 'id_arg_delete' in request.POST:
			deleteArgument(request)
			return redirect(showDebate,id_debate)
		#solicitud de eliminar un contrargumento
		if 'id_counterarg_delete' in request.POST:
			deleteCounterarg(request)
			return redirect(showDebate,id_debate)
		#solicitud de reportar un debate
		if 'report_debate' in request.POST:
			report = reportMessage(request, 'debate')
			return redirect(showDebate,id_debate)
		#solicitud de reportar un argumento
		if 'report_argument' in request.POST:
			report = reportMessage(request, 'argument')
			return redirect(showDebate,id_debate)
		#solicitud de reportar un contraargumento
		if 'report_counterargument' in request.POST:
			report = reportMessage(request, 'counterarg')
			return redirect(showDebate,id_debate)
		#solicitud de cambiar imagen del debate
		if 'update_img_deb' in request.POST:
			form = updateImage(request.POST, request.FILES)
			if form.is_valid():
				id = request.POST['deb_img']
				post = Debate.objects.get(pk=id)
				post.img = form.cleaned_data['img']
				post.save()
				return redirect(showDebate,id_debate)

	owner_user_id = debate.id_user_id #user owner
	owner_user = User.objects.get(id= owner_user_id)
	counterarg_num = debate.counterargs_max
	args_num = debate.args_max
	change_position_num = debate.position_max
	counterarg_type = debate.counterargs_type
	owner_profile = Profile.objects.get(user= owner_user)

	usuario_actual_alias = Profile.objects.get(user= request.user)
	actual_user = request.user

	actual_usr_args_num = Argument.objects.filter(id_debate_id= id_debate, id_user_id=request.user ).count()
	if actual_usr_args_num < args_num:
		can_argue = True
	else:
		can_argue = False

	try:
		actual_user_position = Position.objects.get(id_user_id= actual_user.id, id_debate_id=id_debate)
		position_exist = True
		change_position = actual_user_position.count_change
	except:
		actual_user_position = "No definido"
		position_exist = False
		change_position = 0

	if change_position < change_position_num:
		can_change_position = True
	else:
		can_change_position = False
	counterarg_target = "Ambos"
	if position_exist:
		if actual_user_position.position == 1:
			actual_user_position = "A Favor"
			if counterarg_type == 1:
				counterarg_target = "En Contra"
		else:
			actual_user_position = "En Contra"
			if counterarg_type == 1:
				counterarg_target = "A Favor"


	total_positions = Position.objects.all().order_by('-date')

	debate_members = "publico"
	participate = True
	members_list = []
	if debate.members_type == 1:
		debate_members = PrivateMembers.objects.filter(id_debate_id=id_debate)
		for member in debate_members:
			user = User.objects.get(id=member.id_user_id)
			profile = Profile.objects.get(user_id=user.id)
			members_list.append({'user':user, 'profile':profile, 'type':member.type})

		participate = PrivateMembers.objects.filter(id_debate_id=id_debate,id_user_id=actual_user.id).values('type')

		if len(participate)==0:
			participate = False
			options_owner = []
		elif len(participate)==1:
			type = participate[0]['type']
			if type=='username':
				options_owner=[('username', User.objects.get(id=request.user.id).username)]
			else:
				options_owner=[('alias',Profile.objects.get(user= request.user).alias)]
		else:
			options_owner=[('username', User.objects.get(id=request.user.id).username),
		         		   ('alias',Profile.objects.get(user= request.user).alias)]

	else:
		if debate.participation_type=='all':
			options_owner=[('username', User.objects.get(id=request.user.id).username),
			         ('alias',Profile.objects.get(user= request.user).alias)]
		elif debate.participation_type=='username':
			options_owner=[('username', User.objects.get(id=request.user.id).username)]
		elif debate.participation_type=='alias':
			options_owner=[('alias',Profile.objects.get(user= request.user).alias)]

	max_length = Debate.objects.get(id_debate=id_debate).length
	arg_form0 = newArgForm0(owner=options_owner,max_length=max_length)
	arg_form1 = newArgForm1(owner=options_owner,max_length=max_length)
	counterarg_form = newCounterargForm(owner=options_owner,max_length=max_length)
	report_form = newReportReasonForm()
	updateImg_form = updateImage()

	can_report_deb = True
	r = Report.objects.filter(owner_id=actual_user,debate_id=debate.id_debate,type="debate").count()
	if r>0: can_report_deb = False
	tags = debate.tags.all()
	stats = debateStats(request,id_debate)

	data = {'debate': debate,
		'owner_user': owner_user,
		'user': actual_user,
		'owner_profile': owner_profile,
		'actual_user_position': actual_user_position,
		'can_argue': can_argue, 'p_post': can_change_position,
		'counterarg_num':counterarg_num, 'arg_form1':arg_form1,
		'arg_form0':arg_form0,'counterarg_form':counterarg_form,
		'participate': participate, 'debate_members': members_list, 'counterarg_type': counterarg_type,
		'counterarg_target': counterarg_target, 'visits': visits,
		'report_form':report_form, 'can_report_deb':can_report_deb,
		'updateImg_form':updateImg_form, 'tags': tags,
		'stats': stats}
	return render(request, 'debate.html', data)

def debateStats(request, id_debate):
	debate = Debate.objects.get(id_debate= id_debate)
	counterarg_num = debate.counterargs_max

	infavor_position=Position.objects.filter(id_debate_id=id_debate, position=1)
	against_position=Position.objects.filter(id_debate_id=id_debate, position=0)
	infavor_position_num=infavor_position.count()
	against_position_num=against_position.count()
	if (int(against_position_num+infavor_position_num)==0):
		against_percent=0
		infavor_percent=0
	else:
		infavor_percent = round(float(infavor_position_num) / float(against_position_num+infavor_position_num),3)*100
		against_percent = round(float(against_position_num) / float(against_position_num+infavor_position_num),3)*100

	infavor_arguments = Argument.objects.filter(id_debate_id= id_debate, position= 1)
	against_arguments = Argument.objects.filter(id_debate_id= id_debate, position= 0)
	if len(infavor_arguments.order_by('-score'))==0:
		best_infavor_arg = 'No existen argumentos a favor'
	else:
		best_infavor_arg = infavor_arguments.order_by('-score')[0]
	if len(against_arguments.order_by('-score'))==0:
		best_against_arg = 'No existen argumento en contra'
	else:
		best_against_arg = against_arguments.order_by('-score')[0]

	infavor_args_list = argumentData(infavor_arguments, request.user.id, counterarg_num, id_debate)
	against_args_list = argumentData(against_arguments, request.user.id, counterarg_num, id_debate)
	against_args_list = sorted(against_args_list, key=lambda rate: rate['rate'], reverse=True)
	infavor_args_list = sorted(infavor_args_list, key=lambda rate: rate['rate'], reverse=True)
	infavor_to_against = 0
	against_to_infavor = 0
	reason_infavor_to_against = []
	reason_against_to_infavor = []
	for i in range (1,4):
		num = Position.objects.filter(id_debate_id=id_debate, position=0, change=i).count()
		reason_infavor_to_against.append(num)
		infavor_to_against += num
	for i in range (1,4):
		num = Position.objects.filter(id_debate_id=id_debate, position=1, change=i).count()
		reason_against_to_infavor.append(num)
		against_to_infavor += num

	best_argument = 0
	best_argument_owner = 0
	second_argument = 0
	second_argument_owner = 0
	best_arg_owner_url = None
	second_arg_owner_url = None
	arguments = Argument.objects.filter(id_debate_id=debate.id_debate).order_by('-score')
	if len(arguments)>1:
		best_argument = arguments[0]
		best_argument_owner = User.objects.get(pk=best_argument.id_user_id)
		best_arg_owner_url = best_argument_owner.id
		best_argument_owner = best_argument_owner.username
		profile = Profile.objects.get(pk=User.objects.get(pk=best_argument.id_user_id))
		if best_argument.owner_type == 'alias':
			best_argument_owner = profile.alias
			best_arg_owner_url = profile.alias
		second_argument = arguments[1]
		second_argument_owner = User.objects.get(pk=second_argument.id_user_id)
		second_arg_owner_url = second_argument_owner.id
		second_argument_owner = second_argument_owner.username
		profile = Profile.objects.get(pk=User.objects.get(pk=second_argument.id_user_id))
		if second_argument.owner_type == 'alias':
			second_argument_owner = profile.alias
			second_arg_owner_url = profile.alias
	position_date = Position.objects.filter(id_debate_id = id_debate).values("date")
	position_date_group = itertools.groupby(position_date, lambda record: record.get("date").strftime("%Y-%m-%d"))
	temp = 0
	positions_by_day = []
	for day,position in position_date_group:
		temp += len(list(position))
		positions_by_day.append([day, temp])
	total_position_num = infavor_position_num + against_position_num
	total_arg_num = len(infavor_args_list)+len(against_args_list)
	total_change_num = infavor_to_against + against_to_infavor
	print(positions_by_day)
	stats = { 'infavor_position_num':infavor_position_num, 'against_position_num':against_position_num,
			'infavor_percent': infavor_percent, 'against_percent': against_percent,
			'infavor_args_list': infavor_args_list, 'against_args_list':against_args_list,
			'best_argument': best_argument, 'second_argument': second_argument,
			'best_argument_owner': best_argument_owner, 'best_arg_owner_url':best_arg_owner_url,
			'second_argument_owner': second_argument_owner, 'second_arg_owner_url':second_arg_owner_url,
			'infavor_to_against': infavor_to_against, 'against_to_infavor':against_to_infavor,
			'reason_infavor_to_against': reason_infavor_to_against, 'reason_against_to_infavor':reason_against_to_infavor,
			'positions_by_day':positions_by_day, 'total_change_num':total_change_num,
			'total_position_num':total_position_num, 'total_arg_num':total_arg_num,
			'best_infavor_arg':best_infavor_arg, 'best_against_arg':best_against_arg}

	return stats

def argumentData(arguments, actual_user, counterarg_num, id_debate):
	args_list = []
	for arg in arguments:
		counterargs = Counterargument.objects.filter(id_argument_id= arg.id_argument)
		counterargs_actual_user_num = Counterargument.objects.filter(id_user_id=actual_user, id_argument_id= arg.id_argument).count()
		counterargs_list = []
		can_counterarg = True
		for counterarg in counterargs:
			id = counterarg.id_counterarg
			text = counterarg.text
			owner = User.objects.get(id=counterarg.id_user_id)
			url = counterarg.id_user_id
			if counterarg.owner_type == "alias":
				alias = Profile.objects.get(user= owner)
				owner = alias.alias
				url = owner
			else:
				owner = owner.username
			can_report_counterarg = True
			r = Report.objects.filter(owner_id=actual_user,counterarg_id=counterarg.id_counterarg,type="counterarg").count()
			if r>0: can_report_counterarg = False
			counterargs_list.append({'text': text, 'owner': owner, 'url':url,
									'id': id, 'id_owner': counterarg.id_user_id,
									'owner_type': counterarg.owner_type,
									'can_report_counterarg':can_report_counterarg})
			if counterargs_actual_user_num < counterarg_num:
				can_counterarg = True
			else:
				can_counterarg = False
		owner_arg = User.objects.get(id= arg.id_user_id)
		owner_arg_id = owner_arg.id
		url = owner_arg_id
		if (arg.owner_type == "alias"):
			owner_profile = Profile.objects.get(user=owner_arg)
			owner_arg = owner_profile.alias
			url = owner_profile.alias
		try:
			rate = Rate.objects.get(id_argument_id= arg.id_argument, id_user_id = actual_user, rate_type="positive")
			positive_rate_exist = "si"
		except:
			positive_rate_exist = "no"
		try:
			rate = Rate.objects.get(id_argument_id= arg.id_argument, id_user_id = actual_user, rate_type="negative")
			negative_rate_exist = "si"
		except:
			negative_rate_exist = "no"
		exist_rate=[positive_rate_exist,negative_rate_exist]
		positive_rate = Rate.objects.filter(id_argument_id= arg.id_argument, rate_type="positive").count()
		negative_rate = Rate.objects.filter(id_argument_id= arg.id_argument, rate_type="negative").count()
		total_rate = positive_rate - negative_rate
		arg.score = total_rate
		arg.save()
		position_owner_arg = Position.objects.get(id_user_id= arg.id_user_id, id_debate_id=id_debate).position

		can_report_arg = True
		r = Report.objects.filter(owner_id=actual_user,argument_id=arg.id_argument,type="argument").count()
		if r>0: can_report_arg = False

		args_list.append({'text': arg.text, 'owner_arg': owner_arg, 'rate': total_rate, 'url': url,
							'id_arg': arg.id_argument, 'exist_rate': exist_rate, 'owner_arg_id': owner_arg_id, 'counterargs': counterargs_list,
							'can_counterarg': can_counterarg, 'owner_type':arg.owner_type,
							'can_report_arg':can_report_arg, 'position_owner': position_owner_arg})
	return args_list
def newArgument(request, id_debate, position):
	if request.method == "POST":
		if position==1:
			arg_form = newArgForm1(request.POST, owner=0, max_length=0)
		elif position==0:
			arg_form = newArgForm0(request.POST, owner=0, max_length=0)

		if arg_form.is_valid():
			post = arg_form.save(commit=False)
			post.id_user_id = request.user.id
			post.id_debate_id = id_debate
			post.position = position
			post.save()
	return arg_form
##@brief Funcion que guarda el arguments del user de un argument.
##@param request solicitud web, entrega los datos del user actual
##@return id_debat para redireccional a la vista "showDebate" con este id de debate
##@warning Login is required
@login_required
def newCounterargument(request,id_debate, id_argument):
	if request.method == "POST":
		id_arg = request.POST[id_argument]
		counterarg_form = newCounterargForm(request.POST, owner=0, max_length=0)
		if counterarg_form.is_valid():
			post = counterarg_form.save(commit=False)
			post.id_user_id = request.user.id
			post.id_argument_id = id_arg
			post.save()
		updateReputation(request.user.id, 3)
	return counterarg_form

def updateReputation(id_usr, score):
    profile = Profile.objects.get(user_id=id_usr)
    reputation = profile.reputation + score
    profile.reputation = reputation
    profile.save()

##@brief Funcion que guarda la valoracion del user al argument
##@param request solicitud web, entrega los datos del user actual
##@return respuesta se ingresa en el HttpResponse para indicar la valoracion actualizada del argument
##@warning Login is required
@login_required
def rateArgument(request):
	rate_argument= request.POST['id_arg']
	rate=request.POST['option_rate']
	if rate == "positive":
		score = 4
	elif rate =="negative":
		score = -2
	elif rate =="null-positive":
		score = -4
	elif rate =="null-negative":
		score = 2
	try:
		rate_post = Rate.objects.get(id_argument_id=rate_argument, id_user_id=request.user.id);
		actual_rate = rate_post.rate_type
		if rate == "positive" or rate == "negative":
			if actual_rate == "positive":
				score -= 4
			elif actual_rate == "negative":
				score += 2
		rate_post.rate_type = rate
	except:
		rate_post = Rate(id_argument_id=rate_argument, id_user_id=request.user.id, rate_type=rate)
	rate_post.save()
	id_owner_arg = Argument.objects.get(id_argument=rate_argument).id_user_id
	updateReputation(id_owner_arg, score)
	positive_rate = Rate.objects.filter(id_argument_id= rate_argument, rate_type="positive").count()
	negative_rate = Rate.objects.filter(id_argument_id= rate_argument, rate_type="negative").count()
	total_rate = positive_rate - negative_rate
	return(total_rate)

def deleteArgument(request):
	id_arg = request.POST['id_arg_delete']
	arg = Argument.objects.get(pk=id_arg)
	actual_user = request.user
	if actual_user.is_staff==1:
		arg_text = str(arg.text)
		text = '"'+(arg_text[:30] + '..') if len(arg_text) > 75 else arg_text +'"'
		debate = Debate.objects.get(pk=arg.id_debate_id)
		msg = "Tu argumento "+text+" ha sido eliminado por no cumplir las reglas de la red"
		newNotification(debate,arg.id_user_id,'delete_arg',msg,msg)
		updateReputation(arg.id_user_id, -5)
	else:
		updateReputation(actual_user.id, -3)
	arg.delete()

def deleteCounterarg(request):
	id_counterarg = request.POST['id_counterarg_delete']
	counterarg = Counterargument.objects.get(pk=id_counterarg)
	actual_user = request.user
	if actual_user.is_staff==1:
		counterarg_text = str(counterarg.text)
		text = '"'+(counterarg_text[:30] + '..') if len(counterarg_text) > 75 else counterarg_text +'"'
		arg = Argument.objects.get(pk=counterarg.id_argument_id)
		debate = Debate.objects.get(pk=arg.id_debate_id)
		msg = "Tu contraargumento "+text+" ha sido eliminado por no cumplir las reglas de la red"
		newNotification(debate,arg.id_user_id,'delete_arg',msg,msg)
		updateReputation(counterarg.id_user_id, -5)
	else:
		updateReputation(actual_user.id, -3)
	counterarg.delete()

def reportMessage(request, type):
	actual_user = request.user
	reason = request.POST['reason']
	if type=='debate':
		id_debate = request.POST['id_deb']
		debate = Debate.objects.get(id_debate=id_debate)
	elif type=='argument':
		id_arg = request.POST['id_report_arg']
		arg = Argument.objects.get(pk=id_arg)
		debate = Debate.objects.get(pk=arg.id_debate_id)
	elif type=='counterarg':
		id_counterarg = request.POST['id_report_counterarg']
		counterarg = Counterargument.objects.get(pk=id_counterarg)
		arg = Argument.objects.get(pk=counterarg.id_argument_id)
		debate = Debate.objects.get(pk=arg.id_debate_id)
	report_form = newReportReasonForm(request.POST)
	if report_form.is_valid():
		post = report_form.save(commit=False)
		post.owner = request.user
		post.debate = debate
		post.type = type
		if type=="argument":
			post.argument = arg
		elif type=="counterarg":
			post.argument = arg
			post.counterarg = counterarg
		post.save()
	# updateReputation(request.user.id, 3)
	return report_form

def readNotification(request, id_debate, id_notification):
	notification = Notification.objects.get(id=id_notification)
	notification.state = 1
	notification.save()
	return redirect(showDebate,id_debate)

def visitCount(debate, user):
	utc=pytz.UTC
	try:
		visit = Visit.objects.get(id_debate=debate, id_user_id=user.id)
		delta = visit.date + timedelta(minutes=30)
	except:
		visit = Visit.objects.create(id_debate=debate, id_user_id=user.id)
		delta = utc.localize(visit.date) + timedelta(minutes=30)
	ahora = utc.localize(datetime.datetime.today())
	if delta <= ahora:
		visit.num = visit.num + 1
		visit.date = ahora
		visit.save()
	total = Visit.objects.filter(id_debate=debate).aggregate(Sum('num'))
	return total.values()[0]
