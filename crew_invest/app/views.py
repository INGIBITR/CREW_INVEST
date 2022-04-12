from django.shortcuts import render
from .models import *
#from django.contrib.auth.decorators import login_required


#@login_required
def profile(request):
    request.user = User.objects.get(pk=2)
    stocks = request.user.profile.stocks.order_by('-amount')
    return render(request, 'profile.html', {'stocks': stocks})

def main(request):
    return render(request, 'main.html')