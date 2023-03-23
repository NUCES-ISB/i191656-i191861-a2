#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import requests

CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=Q70QUOPWOYWUCFJZ'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)


# In[2]:


import pandas as pd



df = pd.DataFrame (my_list, columns = ['time', 'open','high','low','close','volume'])
print (df)


# In[3]:


df.drop(index=df.index[0], axis=0, inplace=True)
print(df)


# In[4]:


features = df[['open', 'high', 'low', 'volume']]
labels = df['close']


# In[5]:


modified_data = pd.concat([features, labels], axis=1)


# In[6]:


modified_data


# In[7]:


import pandas as pd
from sklearn.model_selection import train_test_split


df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)
df.dropna(inplace=True)

X_train, X_test, y_train, y_test = train_test_split(df.drop('close', axis=1), df['close'], test_size=0.2, shuffle=False)


# In[8]:


X_train


# In[9]:


y_test


# In[10]:


X_test


# In[11]:


y_train


# In[12]:


from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)


# In[13]:


import pickle


# In[14]:


pickle.dump(model,open('model.pkl','wb'))


# In[15]:


from sklearn.metrics import mean_squared_error

y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f'RMSE: {rmse:.2f}')


# In[1]:


from fbprophet import Prophet

# Load data
df = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=Q70QUOPWOYWUCFJZ')
df['ds'] = pd.to_datetime(df['time'])
df.drop(columns=['time', 'open', 'high', 'low', 'volume'], inplace=True)
df = df[['ds', 'close']].rename(columns={'close': 'y'})

# Train model
model = Prophet()
model.fit(df)

# Generate predictions
future = model.make_future_dataframe(periods=30, freq='D')
forecast = model.predict(future)

# Visualize results
fig = model.plot(forecast)


# In[ ]:


pip install fbprophet


# In[ ]:




