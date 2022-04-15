from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):

    stocks = request.user.profile.stocks.order_by('-amount')
    return render(request, 'profile.html', {'stocks': stocks})

def main(request):
    return render(request, 'main.html')

@login_required
def payment(request):
    return render(request, 'payment.html')


@login_required
def pay(request):

    form = PaymentForm(request.POST)
    if form.is_valid():
        profile = request.user.profile
        profile.balance += form.cleaned_data['sum']
        profile.save()
    else:
        return render(request, 'payment.html', {'form': form })

    return redirect('profile')
    
def logout_view(request):
    logout(request)
    return redirect('main')
    
def signup(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user=form.save()
            profile=Profile(user=user,balance=0)
            profile.id
            profile.save()
            login(request,user)
            return redirect('main')
    else:
        form = UserRegistration()
    return render(request,'signup.html', {'form':form})

def auth_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username =form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=raw_password)
            login(request,user)
            return redirect('main')           
    else:
        form = AuthenticationForm(request.POST)
    return render(request,'login.html',{'form':form})
    
@login_required
def edit(request):
    if request.method == 'POST':
        user = request.user
        profile = request.user.profile 
        form = UserEdit(request.POST,request.FILES)
        user.profile.avatar=form.instance
        if form.is_valid():
            user.username=request.POST.__getitem__('username')
            user.email=request.POST.__getitem__('email')
            user.first_name=request.POST.__getitem__('first_name')
            user.last_name=request.POST.__getitem__('last_name')
            profile = Profile.objects.get(pk=user.profile.id)
            profile.avatar=form.cleaned_data.get('avatar_field')
            profile.save()
            user.save()
            return redirect('profile')
        else:
            return redirect('main') 
    else: 
        form = UserEdit(request.POST)

    return render(request,'edit.html',{'form':form}) 
    
    
    
    
