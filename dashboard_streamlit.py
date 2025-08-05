import streamlit as st
import pandas as pd
from modules import first_questions,first_page
from modules_anuales import graph_years
from modules_mensuales import graph_monthly,graph_monthly_by_year
from modules_diarias import graph_daily,graph_daily_by_year,graph_daily_by_month,graph_daily_by_month_and_year
from KPIs import KPIs
from time_series import TimeSeriesTiendas,TimeSeriesProductos

st.title("Dashboard de Ventas")

choice = st.sidebar.selectbox("Qué quieres ver?",\
    ["Informaciones globales","Ventas anuales","Ventas mensuales"\
        ,"Ventas diarias","KPIs","Predicciones por tienda","Predicciones por producto"])

conversion = {"Ventas anuales": "anuales",
                "Ventas mensuales": "mensuales",
                "Ventas diarias": "diarias"}

if choice == "Informaciones globales":

   first_page()

if choice == "Ventas anuales": 

   st.header("Ventas anuales")

   periode = conversion[choice]
   por_ciudad = st.checkbox(f"Quieres analizar las ventas {periode} por ciudad?")
   por_tiendas = st.checkbox(f"Quieres analizar las ventas {periode} por tienda?")
   por_tipo_de_productos = st.checkbox(f"Quieres analizar las ventas {periode} por tipo de productos?")

   df = pd.read_csv("df_by_year_and_store.csv")
   responses = first_questions(por_ciudad,por_tiendas,por_tipo_de_productos,df)

   graph_years(responses,df)

   
if choice == "Ventas mensuales": 

   st.header("Ventas mensuales")
   periode = conversion[choice]
   df = pd.read_csv("df_by_year_month_and_store.csv")
   por_ciudad = st.checkbox(f"Quieres analizar las ventas {periode} por ciudad?")
   por_tiendas = st.checkbox("Quieres analizar las ventas mensuales por tiendas?")
   por_tipo_de_productos = st.checkbox("Quieres analizar las ventas mensuales por tipo de productos?")

   responses = first_questions(por_ciudad,por_tiendas,por_tipo_de_productos,df)   


   years = df.sort_values('year')['year'].unique()

   options_anios = st.multiselect(
       "De qué anos quieres analizar las ventas mensuales",
        default=years,
        options=years
        )
   
   promedios = st.checkbox("Mostrar las ventas promedias de los anos seleccionados.",value=True)

   df_years = pd.concat([df[df.year == year] for year in options_anios])
   if promedios:
      graph_monthly(responses,df_years)
   else:
      graph_monthly_by_year(responses,df_years)             
if choice == "Ventas diarias": 

   st.header("Ventas diarias") 

   periode = conversion[choice]
   df = pd.read_csv("df_by_year_month_day_and_store.csv")
   por_ciudad = st.checkbox(f"Quieres analizar las ventas {periode} por ciudad?")
   por_tiendas = st.checkbox("Quieres analizar las ventas diarias por tiendas?")
   por_tipo_de_productos = st.checkbox("Quieres analizar las ventas diarias por tipo de productos?")   

   responses = first_questions(por_ciudad,por_tiendas,por_tipo_de_productos,df) 

   years = df.sort_values('year')['year'].unique()
   months = df.sort_values('month')['month'].unique()

   options_anios = st.multiselect(
       "De qué anos quieres analizar las ventas diarias",
        default=years,
        options=years
        )
   
   promedios_anios = st.checkbox("Mostrar las ventas promedias de los anios seleccionados.",value=True)

   options_meses = st.multiselect(
       "De qué meses quieres analizar las ventas diarias",
        default=months,
        options=months
        )
   
   promedios_meses = st.checkbox("Mostrar las ventas promedias de los meses seleccionados.",value=True)  

   options_anios_meses = []
   for year in options_anios:
      for month in options_meses:
         options_anios_meses.append((year,month))

   df_months_years = pd.concat([df[(df.year == year)&(df.month == month)] for year,month in options_anios_meses])

   if promedios_anios and promedios_meses:
      graph_daily(responses,df_months_years)
   elif promedios_meses:
      graph_daily_by_year(responses,df_months_years)
   elif promedios_anios:
      graph_daily_by_month(responses,df_months_years)
   else:
      graph_daily_by_month_and_year(responses,df_months_years)

if choice == "KPIs":

   st.header("KPIs") 

   df = pd.read_csv("df_by_year_month_day_and_store.csv")

   KPIs()

if choice == "Predicciones por tienda":

   st.header("Predicciones por tienda") 

   TimeSeriesTiendas()         

if choice == "Predicciones por producto":

   st.header("Predicciones por producto") 

   TimeSeriesProductos()               