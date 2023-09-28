from datetime import datetime, timedelta
import streamlit as st 
import pyettj.ettj as ettj
import pandas as pd
from bcb import sgs
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime,timedelta

def get_last_date():
    
    if datetime.today().weekday() == 6:
        last_date = (datetime.today()-timedelta(days=2)).strftime('%d/%m/%Y')
    elif datetime.today().weekday() == 0:
        last_date = (datetime.today()-timedelta(days=3)).strftime('%d/%m/%Y')
    else:
        last_date = (datetime.today()-timedelta(days=1)).strftime('%d/%m/%Y')
    
    return last_date

def get_last_month():	
    
    if (datetime.today()-timedelta(days=30)).weekday() in [0,5,6]:
        last_month = (datetime.today()-timedelta(days=33)).strftime('%d/%m/%Y')
    else:
        last_month = (datetime.today()-timedelta(days=30)).strftime('%d/%m/%Y')
    
    return last_month  

def get_last_year():	
    
    if (datetime.today()-timedelta(days=365)).weekday() in [0,5,6]:
        last_year = (datetime.today()-timedelta(days=368)).strftime('%d/%m/%Y')
    else:
        last_year = (datetime.today()-timedelta(days=365)).strftime('%d/%m/%Y')
        
    return last_year

get_last_year()

@st.cache_data
def get_ettj(previous_date, previous_month, previous_year):
    ettj_df_last_date = ettj.get_ettj(previous_date, curva="PRE")
    rename_dict = dict(zip(ettj_df_last_date.columns,['days','di_252_day','di_360_day']))
    ettj_df_last_date = ettj_df_last_date.rename(columns=rename_dict)

    ettj_df_last_month = ettj.get_ettj(previous_month, curva="PRE")
    rename_dict = dict(zip(ettj_df_last_month.columns,['days','di_252_month','di_360_month']))
    ettj_df_last_month = ettj_df_last_month.rename(columns=rename_dict)

    ettj_df_last_year = ettj.get_ettj(previous_year, curva="PRE")
    rename_dict = dict(zip(ettj_df_last_year.columns,['days','di_252_year','di_360_year']))
    ettj_df_last_year = ettj_df_last_year.rename(columns=rename_dict)

    df_merge = pd.merge(ettj_df_last_date, ettj_df_last_month, on="days")
    df_merge = pd.merge(df_merge, ettj_df_last_year, on="days")

    return df_merge


def chart_ipca(series, Title):
    
    ipca_df = (sgs.get((series),last=120)).reset_index(drop=False)
    
    series_char= str(series)
    
    fig = go.Figure()

    fig.add_trace(go.Bar(name='IPCA',x=ipca_df[ipca_df[series_char]<0]['Date'], y=ipca_df[ipca_df[series_char]<0][series_char], text=ipca_df[ipca_df[series_char]<0][series_char], textposition='outside',textfont=dict(color='#26A69A', size=9, family='Fira Code'),marker_color = '#26A69A', marker_line_color='rgb(0,0,0)'))
    fig.add_trace(go.Bar(name='IPCA',x=ipca_df[ipca_df[series_char]>0]['Date'], y=ipca_df[ipca_df[series_char]>0][series_char], text=ipca_df[ipca_df[series_char]>0][series_char], textposition='outside',textfont=dict(color='#EF5350', size=9, family='Fira Code'), marker_color = '#EF5350', marker_line_color='rgb(0,0,0)'))
    fig.update_layout(
        title=f'IPCA Variação Mensal (%) - {Title}',
        font=dict(family='Arial',size=12, color='white'),
        # plot_bgcolor='#131722',
        # paper_bgcolor='#131722', 
        showlegend=False,
        width=400
    )
    fig.update_yaxes(
        range=[-2, 3],
        visible=True,
        showgrid=True,
        showticklabels=False,
        showline=False,
        mirror=True,
        ticks='outside',
        griddash = "dot",
        linecolor='gray',
        gridcolor='gray'
    )
    fig.update_xaxes(
        range=[ipca_df['Date'].min()+timedelta(days=3000), ipca_df['Date'].max()+timedelta(days=50)],
        tickfont=dict(
                color='gray'  # Change the font color to red
            ),
        visible=True,
        showgrid=False,
        showline=False
        
    )
    fig.update_traces(textfont_size=9, textangle=0, textposition='outside')
    
    return fig