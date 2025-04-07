from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Mentorados, Navigators, DisponibilidadeHorarios, Reuniao, Tarefa
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from .auth import valida_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def mentorados(request):
	if not request.user.is_authenticated:
		return redirect('login')

	if request.method == 'GET':
		navigators = Navigators.objects.filter(user=request.user)
		mentorados = Mentorados.objects.filter(user=request.user)
		estagios_flat = [i[1] for i in Mentorados.estagio_choices]
		qty_estagios = [Mentorados.objects.filter(estagio=i).filter(user=request.user).count() for i, j in Mentorados.estagio_choices]
		context = {
			'estagios': Mentorados.estagio_choices,
			'navigators': navigators,
			'mentorados': mentorados,
			'estagios_flat': estagios_flat,
			'qty_estagios': qty_estagios,
		}

		return render(request, 'mentorados.html', context)
	else:
		nome = request.POST.get('nome')
		foto = request.FILES.get('foto')
		estagio = request.POST.get("estagio")
		navigator = request.POST.get('navigator')

		mentorado = Mentorados(
			nome=nome,
			foto=foto,
			estagio=estagio,
			navigator_id=navigator,
			user=request.user
		)

		mentorado.save()

		messages.add_message(request, constants.SUCCESS, 'mentorado cadastrado com sucesso')

		return redirect('mentorados')

def reunioes(request):
	if request.method == 'GET':
		reunioes = Reuniao.objects.filter(data__mentor=request.user)

		return render(request, 'reunioes.html',{'reunioes': reunioes})
	else:
		data = request.POST.get('data')

		data = datetime.strptime(data, '%Y-%m-%dT%H:%M')

		disponibilidade = DisponibilidadeHorarios.objects.filter(
			data_inicial__gte=(data - timedelta(minutes=50)),
			data_inicial__lte=(data + timedelta(minutes=50))
		)

		if disponibilidades.exists():
			messages.add_message(request, constants.ERROR, 'Você já possui uma reunião em aberto.')
			return redirect('reunioes')

		disponibilidade = DisponibilidadeHorarios(
			data_inicial=data,
			mentor=request.user

		)
		disponibilidade.save()

		messages.add_message(request, constants.SUCCESS, 'Horário disponibilizado com sucesso.')
		return redirect('reunioes')

def auth(request):
	if request.method == 'GET':
		return render(request, 'auth_mentorado.html')
	else:
		token = request.POST.get('token')

		if not Mentorados.objects.filter(token=token).exists():
			messages.add_message(request, constants.ERROR, 'Token invalido')
			return redirect('auth_mentorado')
		
		response = redirect('escolher_dia')
		response.set_cookie('auth_token', token, max_age=3600)
		return response

def escolher_dia(request):
	if not valida_token(request.COOKIES.get('auth_token')):
		return redirect('auth_mentorado')

	if request.method == 'GET':
		disponibilidades = DisponibilidadeHorarios.objects.filter(
			data_inicial__gte=datetime.now(),
			agendado=False,
			mentor=mentorado.user
		).values_list('data_inicial', flat=True)

		datas = []
		for i in disponibilidades:
			data = i.date()
			dia_semana = data.strftime('%A')
			mes = data.strftime('%B')
			data_formatada = data.strftime('%d-%m-%Y')
			datas.append({'data': data_formatada, 'dia_semana': dia_semana, 'mes': mes})

		datas_unicas = []
		datas_vistas = set()
		for item in datas:
			if item['data'] not in datas_vistas:
				datas_unicas.append(item)
				datas_vistas.add(item['data'])

		return render(request, 'escolher_dia.html', {'horarios': datas_unicas})

def agendar_reuniao(request):
	if not valida_token(request.COOKIES.get('auth_token')):
		return redirect('auth_mentorado')
	
	mentorado=valida_token(request.COOKIES.get('auth_token'))

	if request.method == 'GET':
		data = request.GET.get("data")
		data = datetime.strptime(data, '%d-%m-%Y')
		horarios = DisponibilidadeHorarios.objects.filter(
			data_inicial__gte=data,
			data_inicial__lt=data + timedelta(days=1),
			agendado=False
		)

		return render(request, 'agendar_reuniao.html', {'horarios': horarios, 'tags': Reuniao.tag_choices})
	else:
		horario_id = request.POST.get('horario')
		tag = request.POST.get('tag')
		descricao = request.POST.get("descricao")

		#TODO: Realizar validações
		horario = DisponibilidadeHorarios.objects.get(id=horario_id)

		if horario.mentor != mentorado.navigator.user:
			messages.add_message(request, constants.ERROR, 'este horario não pertence ao seu mentor')
			
			data = datetime.now().date()
			horarios = DisponibilidadeHorarios.objects.filter(
				data_inicial__gte=data,
				data_inicial__lt=data + timedelta(days=1),
				agendado=False
			)
			return render(request, 'agendar_reuniao.html', {'horarios': horarios, 'tags': Reuniao.tag_choices})

		reuniao = Reuniao(
			data_id=horario_id,
			mentorado=mentorado,
			tag=tag,
			descricao=descricao
		)
		reuniao.save()

		horario.agendado = True
		horario.save()

		messages.add_message(request, constants.SUCCESS, 'reunião agendada com sucesso')
		return redirect('escolher_dia')

def tarefa(request, id):
	mentorado = Mentorados.objects.get(id=id)
	if mentorado.user != request.user:
		raise Http404()
	
	if request.method == 'GET':
		tarefas = Tarefa.objects.filter(mentorado=mentorado)
		videos = Upload.objects.filter(mentorado=mentorado)

		return render(request, 'tarefa.html', {'mentorado': mentorado, 'tarefas': tarefas, 'videos': videos})
	else:
		tarefa = request.POST.get('tarefa')
		tarefa = Tarefa(
			mentorado=mentorado,
			tarefa=tarefa,
			)

		tarefa.save()

		return redirect(f'/mentorados/tarefa/{mentorado.id}')

def upload(request, id):
	mentorado = Mentorados.objects.get(id=id)
	if mentorado.user != request.user:
		raise Http404()
	
	video = request.FILES.get('video')
	upload = Upload(
		mentorado=mentorado,
		video=video
	)
	upload.save()
	return redirect(f'/mentorados/tarefa/{mentorado.id}')

def tarefa_mentorado(request):
	mentorado = valida_token(request.COOKIES.get('auth_token'))
	if not mentorado:
		return redirect('auth_mentorado')
	
	if request.method == 'GET':
		videos = Upload.objects.filter(mentorado=mentorado)
		tarefas = Tarefa.objects.filter(mentorado=mentorado)
		return render(request, 'tarefa_mentorado.html', {'mentorado': mentorado, 'videos': videos, 'tarefas': tarefas})

@csrf_exempt
def tarefa_alterar(request, id):
    mentorado = valida_token(request.COOKIES.get('auth_token'))
    if not mentorado:
        return redirect('auth_mentorado')

    tarefa = Tarefa.objects.get(id=id)
    if mentorado != tarefa.mentorado:
        raise Http404()
    tarefa.realizada = not tarefa.realizada
    tarefa.save()

    return HttpResponse('teste')