import plotly.graph_objects as go
import pandas as pd
import time
from datetime import datetime
from polygon import RESTClient


'''
def priceoutput(ticker):
    key = "lZpPwAaVeNMP6wuWAP3S8IkKbZMDlQwy"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        from_ = int(time.time()) - 86400
        to = int(time.time())
        # {"ticker":"AAPL","queryCount":120,"resultsCount":12,"adjusted":1,"results":[{"v":4905,"vw":145.7662,"o":145.64,"c":145.75,"h":145.85,"l":145.64,"t":1626940800000,"n":152},{"v":3327,"vw":145.6748,"o":145.73,"c":145.65,"h":145.73,"l":145.6,"t":1626942000000,"n":101},{"v":1672,"vw":145.6945,"o":145.71,"c":145.65,"h":145.71,"l":145.65,"t":1626943200000,"n":27},{"v":2168,"vw":145.6405,"o":145.66,"c":145.62,"h":145.66,"l":145.62,"t":1626944400000,"n":56},{"v":2172,"vw":145.712,"o":145.67,"c":145.74,"h":145.79,"l":145.67,"t":1626945600000,"n":55},{"v":3132,"vw":145.7039,"o":145.71,"c":145.7,"h":145.72,"l":145.7,"t":1626946800000,"n":67},{"v":5192,"vw":145.593,"o":145.66,"c":145.6,"h":145.66,"l":145.51,"t":1626948000000,"n":100},{"v":1876,"vw":145.6279,"o":145.62,"c":145.6,"h":145.67,"l":145.6,"t":1626949200000,"n":40},{"v":1259,"vw":145.6862,"o":145.67,"c":145.7,"h":145.7,"l":145.67,"t":1626950400000,"n":20},{"v":43356,"vw":145.709,"o":145.69,"c":145.69,"h":145.75,"l":145.66,"t":1626951600000,"n":489},{"v":60127,"vw":145.6838,"o":145.67,"c":145.85,"h":145.9,"l":145.55,"t":1626952800000,"n":713},{"v":54421,"vw":145.7494,"o":145.86,"c":145.68,"h":145.87,"l":145.67,"t":1626954000000,"n":528}],"status":"OK","request_id":"82b2cddcbbebb45513eab890c423e2d6","count":12}
        #print(resp["results"])
        resp = client.stocks_equities_aggregates(
            ticker, 1, "minute", from_, to, unadjusted=False)
      #  print(resp.results)
     #   print(f"Minute aggregates for {resp['ticker']} between {from_} and {to}.")

        for result in resp.results:
            dt = ts_to_datetime(result['t'])
            print(
                f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
    return resp


'''


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
            "AAPL", 10, "minute", from_, to, unadjusted=False)

        print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")

        for result in resp.results:
            dt = ts_to_datetime(result["t"])
            print(
                f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
    return resp.results


def outputFig(ticker):

    df = priceoutput('AAPL')
    df1 = [0] * len(df)
    j = 0
    for i in df:
        df1[j] = int(i['t'])
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
        title='The Great Recession',
        yaxis_title='AAPL Stock',


    )
    return fig

    
