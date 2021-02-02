#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import numpy as np
from numpy import random

import plotly.offline as pyo
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth

from dash.dependencies import Input, Output, State

import pandas_datareader.data as web

from datetime import datetime
from datetime import date


# In[16]:


USENAME_PASSWORD_PAIRS = [['username', 'password'], ['jamesbond', '007']]


# In[17]:


nsdq = pd.read_csv('Coursera_Plotly_Dash/Data/NASDAQcompanylist.csv')
display(nsdq.head())

nsdq.set_index('Symbol', inplace = True)
options = []

for i in nsdq.index:
    mydict = {}
    mydict['label'] = nsdq.loc[i]['Name'] + ' ' + i
    mydict['value'] = i
    options.append(mydict)


# In[ ]:


app = dash.Dash()

auth = dash_auth.BasicAuth(app, USENAME_PASSWORD_PAIRS)

server = app.server

app.layout = html.Div([html.H1('Stock Ticker Dashboard'),
                       html.Div([html.H3('Select stock symbols:', 
                                         style={'paddingRight':'30px'}),
                                 dcc.Dropdown(id='my_ticker_symbol',
                                              options=options,
                                              value=['TSLA'],
                                              multi=True)], 
                                style={'display':'inline-block', 
                                       'verticalAlign':'top', 
                                       'width':'30%'}),
                       html.Div([html.H3('Select start and end dates:'),
                                 dcc.DatePickerRange(id='my_date_picker',
                                                     min_date_allowed=datetime(2015, 1, 1),
                                                     max_date_allowed=datetime.today(),
                                                     start_date=datetime(2018, 1, 1),
                                                     end_date=datetime.today())],
                                style={'display':'inline-block'}),
                       html.Div([html.Button(id='submit_button',
                                             n_clicks=0,
                                             children='Submit',
                                             style={'fontSize':24, 
                                                    'marginLeft':'30px'})], 
                                style={'display':'inline-block'}),
                       dcc.Graph(id='my_graph',
                                 figure={'data': [{'x': [1,2], 
                                                   'y': [3,1]}]})])

@app.callback(Output('my_graph', 'figure'),
              [Input('submit_button', 'n_clicks')],
              [State('my_ticker_symbol', 'value'),
               State('my_date_picker', 'start_date'),
               State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[0:10],'%Y-%m-%d')
    end = datetime.strptime(end_date[0:10],'%Y-%m-%d')
    
    traces = []
    for i in stock_ticker:
        df = web.get_data_tiingo(i, start, end, api_key="bf53ba6f1912081df72b0411ff15162adf755a1c")
        traces.append({'x': df.index.get_level_values(1),
                       'y': df.close,
                       'name': i})
        
    # Change the output data
    fig = {'data': traces, 'layout': {'title':stock_ticker}}
    return fig



if __name__ == '__main__':
    app.run_server()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




