from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import redirect
#from django.contrib.auth.decorators import login_required


#@login_required
def profile(request):
    request.user = User.objects.get(pk=2)

    stocks = request.user.profile.stocks.order_by('-amount')
    return render(request, 'profile.html', {'stocks': stocks})

def main(request):
    return render(request, 'main.html')

#@login_required
def payment(request):
    return render(request, 'payment.html')


#@login_required
def pay(request):
    request.user = User.objects.get(pk=2)

    form = PaymentForm(request.POST)
    if form.is_valid():
        profile = request.user.profile
        profile.balance += form.cleaned_data['sum']
        profile.save()
    else:
        return render(request, 'payment.html', {'form': form })

    return redirect('profile')
