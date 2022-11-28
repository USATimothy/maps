#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import plotly
import plotly.express as px
import pandas

df = pandas.read_csv('Popular vote backend.csv')

def isstateorDC(name):
    return len(str(name))==2

df_statesDC=df[df['stateid'].apply(isstateorDC)]

df_statesDC["Dmargin"]=df_statesDC['dem_votes']-df_statesDC['rep_votes']
df=df_statesDC.sort_values(by='state')
f1 = px.bar(df,x='state',y='Dmargin',color='called',color_discrete_sequence=['red','blue'])
f1.update_xaxes(categoryorder='category ascending')
plotly.offline.plot(f1,filename='statemargin.html')

#color='called',color_discrete_sequence=['red','blue']