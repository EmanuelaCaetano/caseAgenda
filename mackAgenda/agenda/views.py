
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Tarefa
from .forms import CadastroForm, TarefaForm

# Tela de login
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']
        try:
            # Busca o usuário pelo email
            user = User.objects.get(email=email)
            # Autentica utilizando o email do usuário encontrado e a senha fornecida
            user = authenticate(request, email=user.email, password=senha)
            if user is not None:
                login(request, user)
                return redirect('tarefas')  # Redireciona para a página de tarefas
            else:
                return render(request, 'usuarios/login.html', {'error': 'Usuário ou senha incorretos.'})
        except User.DoesNotExist:
            return render(request, 'usuarios/login.html', {'error': 'Usuário ou senha incorretos.'})
    return render(request, 'usuarios/login.html')
# Tela de cadastro
def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o novo usuário
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

# Tela de tarefas (apenas para usuários logados)
@login_required
def tarefas_view(request):
    tarefas = Tarefa.objects.filter(user=request.user)
    return render(request, 'usuarios/tarefas.html', {'object_list': tarefas})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')
