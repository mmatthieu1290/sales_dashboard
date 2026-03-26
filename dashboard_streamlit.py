import streamlit as st
import pandas as pd
import sqlite3
from modules import first_questions,first_page
from modules_anuales import graph_years
from modules_mensuales import graph_monthly,graph_monthly_by_year
from modules_diarias import graph_daily,graph_daily_by_year,graph_daily_by_month,graph_daily_by_month_and_year
from KPIs import KPIs
from time_series import TimeSeriesTiendas,TimeSeriesProductos,TimeSeriesCiudades

st.title("Sales Dashboard")

choice = st.sidebar.selectbox("What do you want to see?",\
    ["Global information", "Annual sales", "Monthly sales"\
        ,"Daily Sales", "KPIs", "Predictions by Store", "Predictions by Product", "Predictions by City"])

conversion = {"Annual sales": "yearly",
                "Monthly sales": "monthly",
                "Daily Sales": "daily"}

connexion = sqlite3.connect('db.db')
connexion.commit()


if choice == "Global information":

   first_page(connexion)

if choice == "Annual sales": 



   st.header("Annual sales")

   periode = conversion[choice]
   por_ciudad = st.checkbox(f"Do you want to analyze {periode} sales by city?")
   por_tiendas = st.checkbox(f"Do you want to analyze {periode} sales by store?")
   por_tipo_de_productos = st.checkbox(f"Do you want to analyze {periode} sales by product type?")

#   df = pd.read_csv("df_by_year_and_store.csv")
   df = pd.read_sql_query('select * from df_by_year_and_store' \
    , con = connexion)
   responses = first_questions(por_ciudad,por_tiendas,por_tipo_de_productos,df)

   graph_years(responses,df)

   
if choice == "Monthly sales": 

   st.header("Monthly sales")
   periode = conversion[choice]
   df = pd.read_sql_query('select * from df_by_year_month_and_store' \
    , con = connexion)   
   por_ciudad = st.checkbox(f"Do you want to analyze {periode} sales by city?")
   por_tiendas = st.checkbox(f"Do you want to analyze {periode} sales by store?")
   por_tipo_de_productos = st.checkbox(f"Do you want to analyze {periode} sales by product type?")

   responses = first_questions(por_ciudad,por_tiendas,por_tipo_de_productos,df)   


   years = df.sort_values('year')['year'].unique()

   options_anios = st.multiselect(
       "For which years do you want to analyze monthly sales?",
        default=years,
        options=years
        )
   
   promedios = st.checkbox("Show average sales for selected years.",value=True)

   df_years = pd.concat([df[df.year == year] for year in options_anios])
   if promedios:
      graph_monthly(responses,df_years)
   else:
      graph_monthly_by_year(responses,df_years)             
if choice == "Daily Sales": 

   st.header("Daily Sales") 

   periode = conversion[choice]
   df = pd.read_sql_query('select * from df_by_year_month_day_and_store' \
    , con = connexion) 
   por_ciudad = st.checkbox(f"Do you want to analyze {periode} sales by city?")
   por_tiendas = st.checkbox(f"Do you want to analyze {periode} sales by store?")
   por_tipo_de_productos = st.checkbox(f"Do you want to analyze {periode} sales by product type?")  

   responses = first_questions(por_ciudad,por_tiendas,por_tipo_de_productos,df) 

   years = df.sort_values('year')['year'].unique()
   months = df.sort_values('month')['month'].unique()

   options_anios = st.multiselect(
       "For which years do you want to analyze daily sales?",
        default=years,
        options=years
        )
   
   promedios_anios = st.checkbox("Show average sales for the selected years.",value=True)

   options_meses = st.multiselect(
       "For which months do you want to analyze daily sales?",
        default=months,
        options=months
        )
   
   promedios_meses = st.checkbox("Show average sales for selected months.",value=True)  

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

   df = pd.read_sql_query('select * from df_by_year_month_day_and_store' \
    , con = connexion) 

   KPIs(connexion)

if choice == "Predictions by Store":

   st.header("Predictions by Store") 

   TimeSeriesTiendas(connexion)         

if choice == "Predictions by Product":

   st.header("Predictions by Product") 

   TimeSeriesProductos(connexion) 

if choice == "Predictions by City": 

   st.header("Predictions by City") 

   TimeSeriesCiudades(connexion)               