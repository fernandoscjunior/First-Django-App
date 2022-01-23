from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from receitas.models import Receita
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    """Redireciona o usuário à página index"""
    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)

    dados = {
        'receitas': receitas_por_pagina
    }

    return render(request, 'receitas/index.html', dados)

def receita(request, receita_id):
    """Exibe a página de uma receita"""
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_exibir = {
        'receita' : receita
    }

    return render(request, 'receitas/receita.html', receita_exibir)

def cria_receita(request):
    """Cria uma receita"""
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']

        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita)
        receita.save()

        return redirect('dashboard')
    else:
        return render(request, 'receitas/cria_receita.html')

def deleta_receita(request, receita_id):
    """Deleta uma receita"""
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')

def editar_receita(request, receita_id):
    """Manda à página para editar uma receita"""
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = { 'receita':receita }
    return render(request, 'receitas/editar_receita.html', receita_a_editar)

def atualiza_receita(request):
    """Atualiza uma receita"""
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        return redirect('dashboard')