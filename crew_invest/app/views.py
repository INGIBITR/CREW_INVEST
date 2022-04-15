from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.io as plot
import pandas as pd
import time
from datetime import datetime
from polygon import RESTClient


#from django.contrib.auth.decorators import login_required


@login_required
def profile(request):

    stocks = request.user.profile.stocks.order_by('-amount')
    return render(request, 'profile.html', {'stocks': stocks})

def main(request):
    key = '?apikey=4231299af4e6b69b7401daf97277debb'
    url = 'https://financialmodelingprep.com/api/v3/quote-short/'
    return render(request, 'main.html', {'url': url, 'key': key})

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
        if form.is_valid():
            user.username=request.POST.__getitem__('username')
            user.email=request.POST.__getitem__('email')
            user.first_name=request.POST.__getitem__('first_name')
            user.last_name=request.POST.__getitem__('last_name')
            profile = Profile.objects.get(pk=user.profile.id)
            
            if form.cleaned_data.get('avatar_field')!=None:
                profile.avatar=form.cleaned_data.get('avatar_field')
            profile.save()
            user.save()
            return redirect('profile')
        else:
            return redirect('main') 
    else: 
        form = UserEdit(request.POST)

    return render(request,'edit.html',{'form':form}) 
    
    
    
    


def ts_to_datetime(ts) -> str:
    return datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')


def priceoutput(ticker):
    key = "lZpPwAaVeNMP6wuWAP3S8IkKbZMDlQwy"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        from_ = (int(time.time()) - 86400)*1000
        to = int(time.time())*1000
        resp = client.stocks_equities_aggregates(
            ticker, 10, "minute", from_, to, unadjusted=False)

        #print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")

        for result in resp.results:
            dt = ts_to_datetime(result["t"])
            print(
                f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
    return resp.results


def outputFig(ticker):

    df = priceoutput(ticker)
    lastprice = df
    df1 = [0] * len(df)
    j = 0
    for i in df:
        df1[j] = int(i['t'])-3600*1000
        j = j + 1
    df2 = [0] * len(df1)
    i = 0
    for result in df1:
        df2[i] = ts_to_datetime(result)
        i = i + 1
    df1 = pd.DataFrame(df1)
    #f2 = [time['t']/1000 for time in df1]
    df = pd.DataFrame(df)
    lastprice = lastprice[-1]
    lastprice = lastprice['c']
    fig = go.Figure(data=[go.Candlestick(x=df2,
                    open=(df['o']),
                    high=(df['h']),
                    low=df['l'], close=df['c'])
    ])

    fig.update_layout(
        title='Stock graph',
        yaxis_title='{} Stock'.format(ticker),
    )

    return fig, lastprice


def stockpage(request, str):
   # request.user = User.objects.get(pk=2)
    #request.stockpage = StockPage.objects.get(ticker=request)
    app = Dash(__name__)
    fig, lastprice = outputFig(str)


    output = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig)])
    output = plot.to_html(fig, include_plotlyjs=True, full_html=True)
   # output = go.layout()
    request.user = User.objects.get(pk=2)
    if request.method == 'GET':
        return render(request, 'stockpage.html', {'chart': output, 'lastprice': lastprice})
    form = PurchaseForm(request.POST)
    if form.is_valid():
        profile = request.user.profile
        stock = Stock()
        if profile.balance < (form.cleaned_data['stock_quantity'] * lastprice):
            form.errors["stock_quantity"] = ""
            print(form.errors)
            return render(request, 'stockpage.html', {'form': form, 'chart': output, 'lastprice': lastprice})
        else:
            profile.balance -= form.cleaned_data['stock_quantity'] * lastprice
            stock.owner = request.user.profile
            stockToFind = Stock.objects.filter(name=str, owner_id = profile.id).first()
            if stockToFind:
                stockToFind.amount += form.cleaned_data['stock_quantity']
                stockToFind.save()
            else:
                stock.name = str
                stock.price = lastprice
                stock.amount += form.cleaned_data['stock_quantity']
                stock.save()
            profile.save()
            
            return redirect('profile')
    else:
        print(form.errors)
        return render(request, 'stockpage.html', {'form': form, 'chart': output, 'lastprice': lastprice})
    
    
