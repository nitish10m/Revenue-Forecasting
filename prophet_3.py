# -*- coding: utf-8 -*-
"""Prophet_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19R6bqikJNLs5GFmK70MknO2tt9e6p33A
"""

# This implementation is based on the Prophet library

# The Prophet library is an open-source library designed for making forecasts for univariate time series datasets.
# It is easy to use and designed to automatically find # a good set of hyperparameters for the model to make skillful 
# forecasts for data with trends and seasonal structure by default.

#Advantages of using Prophet
#•	Accommodates seasonality with multiple periods
#•	Prophet is resilient to missing values
#•	Best way to handle outliers in Prophet is to remove them 
#•	Fitting of the model is fast 
#•	Intuitive hyper parameters which are easy to tune

# evaluate prophet time series forecasting model on hold out dataset
from pandas import read_csv
from pandas import to_datetime
from pandas import DataFrame
from fbprophet import Prophet
from sklearn.metrics import mean_absolute_error
from matplotlib import pyplot
# check prophet version
import fbprophet

import pandas as pd
import numpy as np

df_rev = pd.read_csv("/content/drive/My Drive/Revenue Forecast Project/Data/Revenue_original.csv")

# Create Report date from raw data

conditions =[(df_rev['Quarter'].str.split(' ').str[1] =="Q1"),\
             (df_rev['Quarter'].str.split(' ').str[1] =="Q2"),\
             (df_rev['Quarter'].str.split(' ').str[1] =="Q3"),\
             (df_rev['Quarter'].str.split(' ').str[1] =="Q4")\
            ]

choices =[("31-03-" + df_rev['Quarter'].str.split(' ').str[0]),\
          ("30-06-" + df_rev['Quarter'].str.split(' ').str[0]),\
          ("30-09-" + df_rev['Quarter'].str.split(' ').str[0]),\
          ("31-12-" + df_rev['Quarter'].str.split(' ').str[0])\
         ]


#df_rev['ReportDate'] = np.select(conditions, choices, default="NA")

df_rev['ReportDate'] = np.select(conditions, choices)
df_rev.head()

#Convert Revernue to float type
df_rev['Revenue'] = df_rev['Revenue'].str.replace(',','')
df_rev['Revenue'] = df_rev['Revenue'].astype('float')

# Convert ReportDate to date type

df_rev['ReportDate'] = pd.to_datetime(df_rev['ReportDate'])
# remove unwanted column
df_rev.drop(['Quarter'], axis=1, inplace=True)

# sort the dataframe in acceding 
df_rev = df_rev.sort_values(['ReportDate'], ascending=[True])

# set column ReportDate as index of dataframe
#df_rev.set_index('ReportDate', inplace=True)
#df_rev.set_index('ReportDate')

# set column 'ReportDate' as Index of dataframe 
df_rev.head(5)

# Reorder the column name
new_column = ['ReportDate','Revenue']
df_rev = df_rev[new_column]
df_rev.head()

#Renaming the columns as desired by Prophet. The Fbprophet library assumes a univariate analysis with respect
# to the time variable and therefore we need not specify other columns in it. 
# So, now let’s rename the columns to ds and y as desired by the library.

df_rev.columns = ["ds","y"]

df_rev['ds'] = pd.to_datetime(df_rev.ds)
df_rev.head()

X = df_rev.values
#print(X)
size = int(len(X) * 0.75)
train, test = X[0:size], X[size:len(X)]
#print(train.dtype)
df_train=pd.DataFrame(train)
df_test= pd.DataFrame(test)

df_train.columns = ['ds','y']
df_test.columns = ['ds', 'y']
print(df_train)
print(df_test)

df_train['ds']= to_datetime(df_train['ds'])
df_test['ds']= to_datetime(df_test['ds'])

# define the model
model = Prophet()
# fit the model
model.fit(df_train)

future = model.make_future_dataframe(periods=28,freq='Q')
future.tail()

# use the model to make a forecast
forecast = model.predict(future)
print(forecast.tail())

print(forecast[['yhat']].tail())

y_pred = forecast['yhat'][-22:].values
print(y_pred)

y_true = df_test['y'][-22:].values
print(y_true)

mae = np.sqrt(mean_absolute_error(y_true, y_pred))
print('RMSE: %.3f' % mae)

# plot expected vs actual
pyplot.plot(y_true, label='Actual')
pyplot.plot(y_pred, label='Predicted')
pyplot.legend()
pyplot.show()

