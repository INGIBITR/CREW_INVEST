from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import redirect
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.io as plot
import pandas as pd
import time
from datetime import datetime
from polygon import RESTClient


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

    fig = go.Figure(data=[go.Candlestick(x=df2,
                    open=(df['o']),
                    high=(df['h']),
                    low=df['l'], close=df['c'])
    ])

    fig.update_layout(
        title='Stock graph',
        yaxis_title='{} Stock'.format(ticker),



    )
    return fig


def stockpage(request, str):
   # request.user = User.objects.get(pk=2)
    #request.stockpage = StockPage.objects.get(ticker=request)
    app = Dash(__name__)
    fig = outputFig(str)


    output = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig)])
    output = plot.to_html(fig, include_plotlyjs = True, full_html = False)
  
    return render(request, 'stockpage.html', {'chart': output  })
