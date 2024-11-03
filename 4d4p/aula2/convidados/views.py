from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from noivos.models import Convidados, Presentes
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from .models import Acompanhantes

def convidados(request):
    token = request.GET.get('token')
    
    if not token:
        messages.error(request, "Token não fornecido.")
        return redirect(reverse('home'))  # Redireciona para a página inicial do app noivos

    convidado = Convidados.objects.get(token=token)
    presentes = Presentes.objects.filter(reservado=False).order_by('-importancia')
    return render(request, 'convidados.html', {'convidado': convidado, 'presentes': presentes, 'token': token})

def responder_presenca(request):
    token = request.GET.get('token')
    resposta = request.GET.get('resposta')
    num_acompanhantes = request.GET.get('num_acompanhantes', 0)
    nomes_acompanhantes = request.GET.get('nomes_acompanhantes', '')
    
    convidado = get_object_or_404(Convidados, token=token)
    
    if resposta not in ['C', 'R']:
        messages.add_message(request, constants.ERROR, 'Você deve confirmar ou recusar')
        return redirect(f'{reverse("convidados")}?token={token}')
    
    try:
        num_acompanhantes = int(num_acompanhantes)
        if num_acompanhantes > convidado.maximo_acompanhantes:
            messages.add_message(request, constants.ERROR, 'Número de acompanhantes excede o limite permitido')
            return redirect(f'{reverse("convidados")}?token={token}')
    except ValueError:
        num_acompanhantes = 0
    
    convidado.status = resposta
    convidado.numero_acompanhantes = num_acompanhantes
    convidado.nomes_acompanhantes = nomes_acompanhantes
    convidado.save()
    
    # Atualizar ou criar acompanhantes
    nomes_acompanhantes_list = nomes_acompanhantes.split(',')
    Acompanhantes.objects.filter(convidado=convidado).delete()  # Remove acompanhantes antigos
    for nome in nomes_acompanhantes_list:
        if nome.strip():  # Evita criar acompanhantes com nomes vazios
            Acompanhantes.objects.create(convidado=convidado, nome=nome.strip(), confirmado=(resposta == 'C'))
    
    messages.add_message(request, constants.SUCCESS, 'Presença respondida com sucesso')
    return redirect(f'{reverse("convidados")}?token={token}')

def reservar_presente(request, id):
    token = request.GET.get('token')
    convidado = get_object_or_404(Convidados, token=token)
    presente = get_object_or_404(Presentes, id=id)

    if presente.reservado:
        messages.add_message(request, constants.ERROR, 'Este presente já foi reservado')
        return redirect(f'{reverse("convidados")}?token={token}')

    presente.reservado = True
    presente.reservado_por = convidado
    presente.save()
    
    messages.add_message(request, constants.SUCCESS, 'Presente reservado com sucesso')
    return redirect(f'{reverse("convidados")}?token={token}')