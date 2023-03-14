# -*- coding: utf-8 -*-
"""Ship heavy industry order prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sh_TbnzIqhK8BpYSc-E5uHBPvsyF3EH8

# **파일 불러오기**
"""

from google.colab import drive
drive.mount('/content/drive')

"""# **데이터 전처리 및 시각화 라이브러리 불러오기**"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

"""# **데이터 가져오기 & 정보 확인**"""

train_df = pd.read_csv("/content/drive/MyDrive/ML,DL datasets/Ship &  Fine Dust Dataset/Ship.csv",encoding = 'cp949')
test_df = pd.read_csv("/content/drive/MyDrive/ML,DL datasets/Ship &  Fine Dust Dataset/Ship.csv",encoding = 'cp949')

train_df.info()

train_df.head(11)

test_df.info()

test_df.head(11)

"""# **데이터 시각화**"""

train_df.hist(bins=50,figsize=(15,10))

plt.figure(figsize=(10,10))
colors = ['silver', 'gold']
train_df['order_yn'].value_counts().plot.pie(explode=(0,0.1),autopct='%.1f%%',shadow=True,colors = colors)

plt.figure(figsize=(10,10))
colors = ['brown', 'pink']
train_df['order_experience'].value_counts().plot.pie(explode=(0,0.1),autopct='%.1f%%',shadow=True,colors = colors)

plt.figure(figsize=(10,10))
colors = ['red','green']
train_df['domestic_competitor_bidding_yn'].value_counts().plot.pie(explode=(0,0.1),autopct='%.1f%%',shadow=True,colors = colors)

plt.figure(figsize=(10,10))
colors = ['cyan','magenta']
train_df['chinese_bid_yn'].value_counts().plot.pie(explode=(0,0.1),autopct='%.1f%%',shadow=True,colors = colors)

plt.figure(figsize = (23,8))
ax =train_df['ship_kinds'].value_counts().plot(kind='bar',color='orange',rot=0)

for p in ax.patches:
    ax.annotate(int(p.get_height()), (p.get_x() + 0.25, p.get_height() - 1),ha = 'center',va = 'bottom',color = 'black')

plt.figure(figsize = (23,8))
ax =train_df['shipowner'].value_counts().plot(kind='bar',color='blue',rot=0)

for p in ax.patches:
    ax.annotate(int(p.get_height()), (p.get_x() + 0.25, p.get_height() - 1),ha = 'center',va = 'bottom',color = 'black')

plt.hist(train_df['ship_fee'])

plt.hist(test_df['ship_fee'])

px.scatter(train_df,x='ship_kinds',y='Exchange_rate',color='order_yn',template='plotly_dark')

px.scatter(train_df,x='shipowner',y='Exchange_rate',color='order_yn',template='plotly_dark')

px.bar(train_df,x='ship_kinds',y='Exchange_rate',color='order_yn',template='plotly_dark')

px.bar(train_df,x='shipowner',y='Exchange_rate',color='order_yn',template='plotly_dark')

"""# **데이터 전처리**"""

train_df.isna().sum()

test_df.isna().sum()

for idx,val in enumerate(train_df.isna().mean()*100):
  print(f"{idx}컬럼의 결측치 비율{val: .4f}%")

for idx,val in enumerate(test_df.isna().mean()*100):
  print(f"{idx}컬럼의 결측치 비율{val: .4f}%")

train_df = train_df.fillna(train_df['ship_fee'].mean())
test_df = test_df.fillna(test_df['ship_fee'].mean())

train_df.isna().sum()

test_df.isna().sum()

"""# **상관계수 확인 및 시각화**"""

train_df.corr()

test_df.corr()

train_df_corr = train_df.corr()

train_df_corr_sort = train_df_corr.sort_values('inernational_oil_pr',ascending=False)

train_df_corr_sort['inernational_oil_pr'].head(6)

plt.figure(figsize=(10,10))
sns.heatmap(train_df.corr(),linewidth=0.5,cmap='summer',annot=True)

plt.figure(figsize=(10,10))
sns.heatmap(train_df.corr(),linewidth=0.5,cmap='summer',annot=True,fmt='.2%')

plt.figure(figsize=(10,10))
sns.clustermap(train_df.corr(),linewidth=0.5,cmap='summer',annot=True,fmt='.2%')

"""# **원핫 인코딩 처리**"""

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import LabelBinarizer

x_train = train_df.drop(['order_yn'],axis = 1)
x_test = test_df.drop(['order_yn'],axis = 1)
y_train = train_df[['order_yn']]
y_test = test_df[['order_yn']]

transformer = make_column_transformer((OneHotEncoder(), ['order_experience','shipowner','ship_kinds','chinese_bid_yn','domestic_competitor_bidding_yn']),remainder='passthrough')
transformer.fit(x_train)
x_train = transformer.transform(x_train)
x_test = transformer.transform(x_test)

lb = LabelBinarizer()
lb.fit(y_train)
labels = lb.classes_
y_train = lb.transform(y_train)
y_test = lb.transform(y_test)

x_train.shape

y_train.shape

"""# **Tensorflow & Keras 라이브러리 불오기 및 모델 설계**"""

import tensorflow as tf
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

input = Input(shape=(35,))

net = Dense(units=512)(input)
net = Activation('relu')(net)
net = Dense(units=256)(net)
net = Activation('relu')(net)
net = Dense(units=1)(input)
net = Activation('sigmoid')(net)
model = Model(inputs=input, outputs=net)
model.summary()

model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])

model.fit(x_train, y_train, epochs=150, validation_data=(x_test, y_test))

x_test = transformer.transform(pd.DataFrame([['no',86.3, 3413, 'M', 'G', 28789, 'yes', 34768, 'yes',224.3,25.7,'no']],columns=['order_experience','inernational_oil_pr','Exchange_rate','shipowner','ship_kinds','ship_fee','chinese_bid_yn','ship size','domestic_competitor_bidding_yn','order_backlog','bid_pr','order_yn']))
print(x_test)

"""# **설계된 모델 예측 확인**"""

y_predict = model.predict(x_test)
print(y_predict) 
print(y_predict.flatten())
print(y_predict.flatten()[0])
print(1 if y_predict.flatten()[0] > 0.5 else 0)
print(labels[1 if y_predict.flatten()[0] > 0.5 else 0])