from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group, User





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    customer_data = {
        'nome': customer.name,
    }
    
    
    context = {'customer': customer_data}
    
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    customer = request.user.customer
    
    # Extraia as notas do Customer atual
    nota_basicos = customer.nota_conhec_basicos
    nota_especificos = customer.nota_conhec_especificos
    nota_final = customer.calcular_nota_final()
    
    context = {'nota_basicos': nota_basicos,'nota_especificos': nota_especificos,'nota_final': nota_final    }
    return render(request, 'accounts/user.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o usuário
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            # Verifica se já existe um objeto Customer associado ao usuário
            existing_customer = Customer.objects.filter(user=user).first()
            if not existing_customer:
                # Se não existir, cria um novo objeto Customer
                customer = Customer.objects.create(user=user, email=email, name=username)
                messages.success(request, 'Conta criada: ' + username)
            else:
                # Se já existir, atualiza o email no objeto Customer existente
                existing_customer.email = email
                existing_customer.save()
                messages.info(request, 'Uma conta já existe para ' + username + '. Email atualizado.')
            
            return redirect('login')
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)
    
@unauthenticated_user
def loginPage(request):
    # If the user is logged in he shouldnt have access to the login page
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Nome de usuário ou senha incorretos')
        
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')





# Renderizando baralhos e cards na home



@login_required(login_url='login')
def home(request):
    
    customer = request.user.customer
    baralhos = Baralho.objects.filter(customer=customer)
    context = {'baralhos': baralhos}
    return render(request, 'accounts/home.html', context)

@login_required(login_url='login')
def baralho_detail(request, id):
    
    baralhos = get_object_or_404(Baralho, id=id, customer=request.user.customer)
    cards = baralhos.cards.all()
    context = {'baralhos': baralhos, 'cards': cards}
    return render(request, 'accounts/baralho_detail.html', context)

@login_required(login_url='login')
def baralho_create(request):
    
    if request.method == 'POST':
        form = BaralhoForm(request.POST)
        if form.is_valid():
            baralho = form.save(commit=False)
            baralho.customer = request.user.customer
            baralho.save()
            return redirect('home')
    else:
        form = BaralhoForm()
    return render(request, 'accounts/baralho_form.html', {'form': form})

@login_required(login_url='login')
def baralho_update(request, id):
    
    baralho = get_object_or_404(Baralho, id=id, customer=request.user.customer)
    if request.method == 'POST':
        form = BaralhoForm(request.POST, instance=baralho)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BaralhoForm(instance=baralho)
    return render(request, 'accounts/baralho_form.html', {'form': form})

@login_required(login_url='login')
def baralho_delete(request, id):
    
    baralho = get_object_or_404(Baralho, id=id, customer=request.user.customer)
 
    if request.method == 'POST':
        baralho.delete()
        return redirect('home')
    
    return render(request, 'accounts/baralho_delete.html', {'baralho': baralho})


# Cards

@login_required(login_url='login')
def card_detail(request, id):
    card = get_object_or_404(Card, id=id)
    return render(request, 'accounts/card_detail.html', {'card': card})


@login_required(login_url='login')
def card_create(request, baralho_id):
    baralho = get_object_or_404(Baralho, id=baralho_id, customer=request.user.customer)
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.baralho = baralho
            card.save()
            return redirect('baralho_detail', id=baralho.id)
    else:
        form = CardForm()
    return render(request, 'accounts/card_form.html', {'form': form, 'baralho': baralho})


@login_required(login_url='login')
def card_update(request, id):
    card = get_object_or_404(Card, id=id, baralho__customer=request.user.customer)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('baralho_detail', id=card.baralho.id)
    else:
        form = CardForm(instance=card)
    return render(request, 'accounts/card_form.html', {'form': form, 'card': card})


@login_required(login_url='login')
def card_delete(request, id):
    card = get_object_or_404(Card, id=id, baralho__customer=request.user.customer)
    if request.method == 'POST':
        baralho_id = card.baralho.id
        card.delete()
        return redirect('baralho_detail', id=baralho_id)
    return render(request, 'accounts/card_delete.html', {'card': card})