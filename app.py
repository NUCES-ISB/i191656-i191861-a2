import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import csv
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))





@app.route('/')
def index():
   
    df = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=Q70QUOPWOYWUCFJZ')
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    df.dropna(inplace=True)
    y_pred = model.predict(df[['open', 'high', 'low', 'volume']])
    output = y_pred[0]

    graph = go.Figure()
    graph.add_trace(go.Scatter(x=df.index, y=df['open'], name='Open'))
    graph.add_trace(go.Scatter(x=df.index, y=df['high'], name='High'))
    graph.add_trace(go.Scatter(x=df.index, y=df['low'], name='Low'))
    graph.add_trace(go.Scatter(x=df.index, y=df['volume'], name='Volume'))
    graph.add_trace(go.Scatter(x=[df.index[-1], df.index[-1]], y=[df['open'][-1], output], name='Prediction', line=dict(color='red', width=2, dash='dash')))
    graph.update_layout(title='Live Dashboard', xaxis_title='Time', yaxis_title='Price')
    
    
    
    
    return render_template('index.html', output=output, open=df.iloc[-1]['open'], high=df.iloc[-1]['high'], low=df.iloc[-1]['low'], volume=df.iloc[-1]['volume'],graph=graph.to_html(full_html=False))


if __name__ == '__main__':
    app.run(debug=True)


