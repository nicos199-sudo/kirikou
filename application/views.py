from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
import datetime
#from .decorators import unauthenticated_user, allowed_users, admin_only


def register(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'registration/register.html', context)


def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'registration/login.html', context)
    
def logoutPage(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')


def userPage(request):
    context = {}
    return render(request, 'application/user.html', context)

def dashboard(request):
    commandes = Commande.objects.all()
    total_commandes = commandes.count()
    context = {'total_commandes':total_commandes}
    return render(request, 'application/index.html', context)

@login_required(login_url='login')


def home(request):
    commandes = Commande.objects.filter(date_commande__date=timezone.now())
    donateurs = Donateur.objects.all()
    hopitaux = Hopitaux.objects.all()
    total_hopitaux = hopitaux.count()
    total_commandes = commandes.count()
    total_donateurs = donateurs.count()
    context = {'total_commandes':total_commandes,
       'total_donateurs':total_donateurs,
       'total_hopitaux':total_hopitaux,
    }
    return render(request ,'application/home.html', context)
    
@login_required(login_url='login')

def donateurs_list(request):
    donateurs = Donateur.objects.all()
    return render(request, 'application/list_donateur.html', {'donateurs' : donateurs})

@login_required(login_url='login')

def create_donateur(request):
    form = DonateurCreateForm()
    if request.method == 'POST':
        form = DonateurCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_donateur')
    context = {'form': form}
    return render (request, 'application/donateur_form.html', context)

@login_required(login_url='login')



def update_donateur(request, pk):
    donateur = Donateur.objects.get(id=pk)
    form = DonateurCreateForm(instance=donateur)
    if request.method == 'POST':
        form = DonateurCreateForm(request.POST,instance=donateur)
        if form.is_valid():
            form.save()
            return redirect('/liste_donateur')
    context = {'form': form}
    return render(request,'application/donateur_form.html', context)

@login_required(login_url='login')



def delete_donateur(request, pk):
    donateur = Donateur.objects.get(id=pk)
    if request.method == 'POST':
        donateur.delete()
        return redirect('/liste_donateur')
    context = {'item':donateur}
    return render(request,'application/delete_donateur.html', context)


@login_required(login_url='login')



def hopitaux_list(request):
    hopitaux = Hopitaux.objects.all()
    return render(request, 'application/liste_hopitaux.html',{'hopitaux': hopitaux})

@login_required(login_url='login')



def create_hopitaux(request):
    form = HopitauxCreateForm()
    if request.method == 'POST':
        form = HopitauxCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_hopitaux')
    context = {'form': form}
    return render(request,'application/create_hopitaux.html', context)

@login_required(login_url='login')



def update_hopitaux(request, pk):
    hopitaux = Hopitaux.objects.get(id=pk)
    form = HopitauxCreateForm(instance=hopitaux)
    if request.method == 'POST':
        form = HopitauxCreateForm(request.POST,instance=hopitaux)
        if form.is_valid():
            form.save()
            return redirect('/liste_hopitaux')
    context = {'form': form}
    return render(request,'application/create_hopitaux.html', context)

@login_required(login_url='login')



def delete_hopitaux(request, pk):
    hopitaux = Hopitaux.objects.get(id=pk)
    if request.method == 'POST':
        hopitaux.delete()
        return redirect('/liste_hopitaux')
    context = {'item':hopitaux}
    return render(request,'application/delete_hopitaux.html', context)

@login_required(login_url='login')



def stock_detail(request):
    stock = Stock.objects.all()
    return render(request, 'application/detail_stock.html', {'stock' : stock})

@login_required(login_url='login')



def create_stock(request):
    form = StockCreateForm()
    if request.method == 'POST':
        form = StockCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/detail_stock')
    context = {'form': form}
    return render(request,'application/create_stock.html', context)

@login_required(login_url='login')



def update_stock(request, pk):
    stock = Stock.objects.get(id=pk)
    form = StockCreateForm(instance=stock)
    if request.method == 'POST':
        form = StockCreateForm(request.POST,instance=stock)
        if form.is_valid():
            form.save()
            return redirect('/detail_stock')
    context = {'form': form}
    return render(request,'application/create_stock.html', context)

@login_required(login_url='login')



def delete_stock(request, pk):
    stock = Stock.objects.get(id=pk)
    if request.method == 'POST':
        stock.delete()
        return redirect('/detail_stock')
    context = {'item':stock}
    return render(request,'application/delete_stock.html', context)

@login_required(login_url='login')



def create_commande(request):
    form = CommandeCreateForm()
    if request.method == 'POST':
        form = CommandeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/commande')
    context = {'form': form}
    return render(request,'application/create_commande.html', context)
    
@login_required(login_url='login')



def commandes_list(request):
    commande = Commande.objects.all()
    return render(request, 'application/list_commande.html', {'commande': commande})


@login_required(login_url='login')



def delete_commande(request, pk):
    commande = Commande.objects.get(id=pk)
    if request.method == 'POST':
        commande.delete()
        return redirect('/commande')
    context = {'item':commande}
    return render(request,'application/delete_commande.html', context)

@login_required(login_url='login')



def update_commande(request, pk):
    commande = Commande.objects.get(id=pk)
    form = CommandeCreateForm(instance=commande)
    if request.method == 'POST':
        form = CommandeCreateForm(request.POST,instance=commande)
        if form.is_valid():
            form.save()
            return redirect('/commande')
    context = {'form': form}
    return render(request,'application/create_commande.html', context)