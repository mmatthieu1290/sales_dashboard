import pandas as pd
import streamlit as st
from datetime import timedelta
import plotly.graph_objects as go
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX
from modules_time_series import PredictAndGraph
import pickle

def TimeSeriesTiendas(connexion):
   
   
   store_sales = pd.read_sql_query('select * from cities_store' \
    , con = connexion)

   tiendas = [f"Store {nb_store}" for nb_store in store_sales.city_store.tolist()]
   choice_tienda = st.selectbox("Choose the store",\
    ["All stores"] + tiendas)

   
   if choice_tienda != "All stores":


      sum_sales_ = pd.read_sql_query('select * from sales_by_date_and_store_and_promotion',
                              dtype={'store_nbr': 'int32','onpromotion' : 'int32',
      'sales': 'float32',},parse_dates=['date'],con=connexion).set_index("store_nbr").loc[int(choice_tienda.split(" ")[1])]   
   else:
      sum_sales_ = pd.read_sql_query('select * from sales_by_date_and_promotion',
                              dtype={'onpromotion' : 'int32',
      'sales': 'float32',},parse_dates=['date'],con=connexion)
   PredictAndGraph(sum_sales_,choice_tienda)   
      

def TimeSeriesProductos(connexion):


   family_sales = pd.read_sql_query('select * from productos' \
    , con = connexion)   

   productos = family_sales.family.tolist()

   choice_producto = st.selectbox("Choose the product",\
    ["All products"] + productos)

   
   if choice_producto != "All products":
      sum_sales_ = pd.read_sql_query('select * from sales_by_date_and_family_and_promotion',
                              dtype={'family': 'str','onpromotion' : 'int32',
      'sales': 'float32',},parse_dates=['date'],con=connexion).set_index("family").loc[choice_producto]
   else:
      sum_sales_ = pd.read_sql_query('select * from sales_by_date_and_promotion',
                              dtype={'onpromotion' : 'int32',
      'sales': 'float32',},parse_dates=['date'],con=connexion)
   PredictAndGraph(sum_sales_,choice_producto)       


def TimeSeriesCiudades(connexion):

   
   ciudades = pd.read_sql_query('select * from cities' \
    , con = connexion)   
   ciudades = ciudades.city.tolist()
   choice_ciudad = st.selectbox("Choose the city",\
    ["All cities"] + ciudades)

   
   if choice_ciudad != "All cities":
      sum_sales_ = pd.read_sql_query('select * from sales_by_date_and_cities_and_promotion',
                              dtype={'city': 'str','onpromotion' : 'int32',
      'sales': 'float32',},parse_dates=['date'],con=connexion).set_index("city").loc[choice_ciudad]      
   else:
      sum_sales_ = pd.read_sql_query('select * from sales_by_date_and_promotion',
                              dtype={'onpromotion' : 'int32',
      'sales': 'float32',},parse_dates=['date'],con=connexion)
   PredictAndGraph(sum_sales_,choice_ciudad)