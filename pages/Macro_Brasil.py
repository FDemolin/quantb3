import os, sys
sys.path.insert(0, os.path.dirname(os.getcwd()))
import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.express as px
import pyettj.ettj as ettj
from bcb import sgs
from datetime import datetime, timedelta
from config.utils.utils import get_last_date, get_last_month, get_last_year, get_ettj, chart_ipca


st.set_page_config(
    page_title="Markets Analysis",
    page_icon="📈",
    layout="wide",
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

previous_date = get_last_date()
previous_month = get_last_month()
previous_year = get_last_year()

try:

    df_di = get_ettj(previous_date, previous_month, previous_year)

    di_chart = px.line(df_di, 
                x="days", 
                y=["di_252_day","di_252_month","di_252_year"],
                labels = {"days":"Dias", "value":"DI base 252"},
                color_discrete_sequence=[  "#a0e0e7","#1784af","#044984"],          
                title="Curva de Juros BRASIL")

    newnames = {"di_252_day": "1 Day", "di_252_month": "1 Month Ago", "di_252_year": "1 Year Ago"}

    di_chart.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                        legendgroup = newnames[t.name],
                                        hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
    di_chart.update_yaxes(
        mirror=True,
        ticks='outside',
        visible=True,
        showline=False,
        showgrid=True,
        griddash = "dot",
        linecolor='lightgray',
        gridcolor='lightgray'
    )
    di_chart.update_layout(legend=dict(
        title='',
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="right",
        x=0.3
    ))

    m2_df = (sgs.get((27842),last=120)).reset_index(drop=False)
    m2_df = m2_df.rename(columns={'27842':'Aggr. M2'})

    m2_chart = px.area(m2_df,
                    x="Date",
                    y="Aggr. M2",
                    title="M2 - BRASIL")
    
    tab1, tab2 = st.tabs(["DI 252", "M2"])	

    with tab1:
        st.plotly_chart(di_chart)
    with tab2:
        st.plotly_chart(m2_chart)


except:
    st.markdown('Not available')


ipca_df = (sgs.get((433),last=120)).reset_index(drop=False)





col1, col3, col2 = st.columns((3,1,3))

with col1:
    st.plotly_chart(chart_ipca(433,'Geral'))
    st.plotly_chart(chart_ipca(1636,'Habitação'))
    st.plotly_chart(chart_ipca(1638,'Vestuário'))
    st.plotly_chart(chart_ipca(1639,'Transportes'))
    st.plotly_chart(chart_ipca(1642,'Despesas pessoais'))
    
with col2:
    st.plotly_chart(chart_ipca(1635,'Alimentação e bebidas'))
    st.plotly_chart(chart_ipca(1637,'Artigos de residência'))
    st.plotly_chart(chart_ipca(1640,'Comunicação'))
    st.plotly_chart(chart_ipca(1641,'Saúde'))
    st.plotly_chart(chart_ipca(1643,'Educação'))