import streamlit as st
from datetime import date
import pandas as pd
from dateutil.relativedelta import relativedelta
import plotly.express as px


def KPIs():

    df = pd.read_csv("sales_by_date.csv", parse_dates=["date"])

    KPI_choice = st.selectbox("Qué KPI quieres ver?",\
    ["Crecimiento anual de ventas","Crecimiento mensual de ventas","Crecimiento anual mes a mes"])

    min_date = df.date.min()
    max_date = df.date.max()

    if KPI_choice == "Crecimiento mensual de ventas":

       mes_inicial = st.date_input("Indique la fecha inicial",value=min_date,min_value = min_date, max_value =max_date)
       mes_final = st.date_input("Indique la fecha final",value=max_date,min_value = min_date, max_value =max_date)

       mes_inicial = date(mes_inicial.year,mes_inicial.month,1)
       mes_final = date(mes_final.year,mes_final.month,1)+ relativedelta(months=1) - relativedelta(days = 1)

       df_selected = df[df.date.apply(lambda x :  pd.Timestamp(mes_inicial) <= x and x <=  pd.Timestamp(mes_final))]

       df_selected["month"] = df_selected.date.apply(lambda x : x.month).astype(int)
       df_selected["year"] = df_selected.date.apply(lambda x : x.year).astype(int)    

       df_selected = df_selected.groupby(["year","month"])["sales"].sum().to_frame().reset_index()
       df_selected = df_selected.sort_values(["year","month"])
       df_selected["date"] = df_selected[["year","month"]].apply(lambda x : f"{x[1]}-{x[0]}",axis = 1)
       df_selected["variacion_mensual"] = 100 * (df_selected["sales"] - df_selected.shift(1)["sales"]) / df_selected.shift(1)["sales"]
       df_selected.index = range(len(df_selected))

       fig = px.bar(df_selected.iloc[1:], x='date', y='variacion_mensual')
       fig.update_xaxes(title_text = "Mes",title_font = {"size": 20},
        title_standoff = 25,ticktext=df_selected.date.unique(),tickvals=df_selected.date.unique(),)
       st.header("Varacion mensual")
       st.plotly_chart(fig, config = {'scrollZoom': False})

    if KPI_choice == "Crecimiento anual mes a mes":

       mes_inicial = st.date_input("Indique la fecha inicial",value=min_date,min_value = min_date, max_value =max_date)
       mes_final = st.date_input("Indique la fecha final",value=max_date,min_value = min_date, max_value =max_date)

       mes_inicial = date(mes_inicial.year,mes_inicial.month,1)
       mes_final = date(mes_final.year,mes_final.month,1)+ relativedelta(months=1) - relativedelta(days = 1)

       df_selected = df[df.date.apply(lambda x :  pd.Timestamp(mes_inicial) <= x and x <=  pd.Timestamp(mes_final))]

       df_selected["month"] = df_selected.date.apply(lambda x : x.month).astype(int)
       df_selected["year"] = df_selected.date.apply(lambda x : x.year).astype(int)    

       df_selected = df_selected.groupby(["year","month"])["sales"].sum().to_frame().reset_index()
       df_selected = df_selected.sort_values(["year","month"])
       df_selected["date"] = df_selected[["year","month"]].apply(lambda x : f"{x[1]}-{x[0]}",axis = 1)
       df_selected["variacion_anual"] = 100 * (df_selected["sales"] - df_selected.shift(12)["sales"]) / df_selected.shift(12)["sales"]
       df_selected.index = range(len(df_selected))

       fig = px.bar(df_selected.iloc[12:], x='date', y='variacion_anual')
       fig.update_xaxes(title_text = "Mes",title_font = {"size": 20},
        title_standoff = 25,ticktext=df_selected.date.unique(),tickvals=df_selected.date.unique(),)
       st.header("Varacion anual: variacion relativa de cada mes con respecto al mismo mes del año anterior")
       st.plotly_chart(fig, config = {'scrollZoom': False})

    if KPI_choice == "Crecimiento anual de ventas":

       ano_inicial = st.date_input("Indique la fecha inicial",value=min_date,min_value = min_date, max_value =max_date)
       ano_final = st.date_input("Indique la fecha final",value=max_date,min_value = min_date, max_value =max_date)

       ano_inicial = date(ano_inicial.year,1,1)
       ano_final = date(ano_final.year,1,1)

       df_selected = df[df.date.apply(lambda x :  pd.Timestamp(ano_inicial) <= x and x <=  pd.Timestamp(ano_final))]

       df_selected["year"] = df_selected.date.apply(lambda x : x.year).astype(int)    

       df_selected = df_selected.groupby(["year"])["sales"].sum().to_frame().reset_index()
       df_selected = df_selected.sort_values(["year"])
       df_selected["variacion_anual"] = 100 * (df_selected["sales"] - df_selected.shift(1)["sales"]) / df_selected.shift(1)["sales"]
       df_selected.index = range(len(df_selected))

       fig = px.bar(df_selected.iloc[1:], x='year', y='variacion_anual')
       fig.update_xaxes(title_text = "Año",title_font = {"size": 20},
        title_standoff = 25,ticktext=df_selected.year.unique(),tickvals=df_selected.year.unique(),)
       st.header("Varacion anual")
       st.plotly_chart(fig, config = {'scrollZoom': False}) 

                
