from flask import Flask, render_template, request
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objs as go
import pandas as pd
import pickle
import json

with open('model.pkl','rb') as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/dashboard/", methods=['GET'])
def dashboard():
    df = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=Q70QUOPWOYWUCFJZ')
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    df.dropna(inplace=True)
    y_pred = model.predict(df[['open', 'high', 'low', 'volume']])

    graph = go.Figure()
    graph.add_trace(go.Scatter(x=df.index, y=df['open'], name='Open'))
    graph.add_trace(go.Scatter(x=df.index, y=df['high'], name='High'))
    graph.add_trace(go.Scatter(x=df.index, y=df['low'], name='Low'))
    graph.add_trace(go.Scatter(x=df.index, y=y_pred, name='Prediction', line=dict(color='red', width=2, dash='dash')))
    graph.update_layout(title='Dashboard', xaxis_title='Time', yaxis_title='Price')
    graphJSON = json.dumps(graph, cls=PlotlyJSONEncoder)

    return render_template('dashboard.html',
                           output=y_pred[-1],
                           open=df.iloc[-1]['open'],
                           high=df.iloc[-1]['high'],
                           low=df.iloc[-1]['low'],
                           volume=df.iloc[-1]['volume'],
                           graphJSON=graphJSON)

@app.route("/prediction/", methods=['GET', 'POST'])
def prediction():
  if request.method == 'POST':
      open = request.form['open']
      high = request.form['high']
      low = request.form['low']
      volume = request.form['volume']
      y_pred = model.predict([[open, high, low, volume]])[0]
      return render_template("prediction.html", result=y_pred)
  return render_template("prediction.html")

if __name__ == '__main__':
	app.run()