from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth

# Create your views here.
def cadastro(request):
	if request.method == 'GET':
		return render(request, 'cadastro.html')
	else:
		username = request.POST.get('username')
		senha = request.POST.get('senha')
		confirmar_senha = request.POST.get('confirmar_senha')

		if senha != confirmar_senha:
			messages.add_message(request, constants.ERROR, 'senhas não coincidem')
			return redirect('/usuarios/cadastro')
		
		if len(senha) < 6:
			messages.add_message(request, constants.ERROR, 'senha deve ser maior que 5 digitos')
			return redirect('/usuarios/cadastro')

		users = User.objects.filter(username=username)

		if users.exists():
			messages.add_message(request, constants.ERROR, 'username ja cadastrado')
			return redirect('/usuarios/cadastro')
		
		User.objects.create_user(
			username=username,
			password=senha
		)

	
		return redirect('/usuarios/login')

def login(request):
	if request.method == 'GET':
		return render(request, 'login.html')
	else:
		username = request.POST.get('username')
		senha = request.POST.get('senha')

		user = authenticate(request, username=username, password=senha)

		if user:
			auth.login(request, user)
			return redirect('/mentorados/')
		
		messages.add_message(request, constants.ERROR, 'username ou senha invalidos')
		return redirect('login')