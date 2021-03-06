from os import name
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
    """ Realiza o cadastro de um novo usuário"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'Coloque um nome.')
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, 'Coloque um email.')
            return redirect('cadastro')

        if senhas_diferentes(senha, senha2):
            messages.error(request, 'A senhas não coincidem.')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já foi cadastrado.')
            return redirect('cadastro')

        if User.objects.filter(user=nome).exists():
            messages.error(request, 'Este email já foi cadastrado.')
            return redirect('cadastro')


        user = User.objects.create_user(username=nome, email=email, password=senha,)
        user.save()
        print('')
        messages.success(request, 'Cadastro realizado com sucesso.')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    """ Realiza o login de um usuário"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos de Email e Senha não podem ficar sozinhos.')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout(request):
    """ Realiza um 'logout' de um usuário'"""
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    """ Realiza um redirect à página dashboard """
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas' : receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    
    else:
        return redirect('index')

def campo_vazio(campo):
    """ Verifica se há algum campo vazio"""
    return not campo.strip()

def senhas_diferentes(senha, senha2):
    """ Verifica se as senhas estão diferentes"""
    return senha != senha2
