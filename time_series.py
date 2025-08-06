import pandas as pd
import streamlit as st
from datetime import timedelta
import plotly.graph_objects as go
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX
from modules_time_series import PredictAndGraph
import pickle

def TimeSeriesTiendas():
   
   
   store_sales = pd.read_csv(
     'cities_store.csv'
)

   tiendas = [f"Tienda {nb_store}" for nb_store in store_sales.city_store.tolist()]
   choice_tienda = st.selectbox("Elige la tienda",\
    ["Todas las tiendas"] + tiendas)

   
   if choice_tienda != "Todas las tiendas":
      sum_sales_ = pd.read_csv("sales_by_date_and_store_and_promotion.csv",usecols=['date','store_nbr', 'onpromotion','sales'],
                              dtype={'store_nbr': 'int32','onpromotion' : 'int32',
      'sales': 'float32',},parse_dates=['date'],
    infer_datetime_format=True).set_index("store_nbr").loc[int(choice_tienda.split(" ")[1])]
   else:
      sum_sales_ = pd.read_csv("sales_by_date_and_promotion.csv",
                              usecols=['date','onpromotion', 'sales'],
                              dtype={'sales': 'float32','onpromotion':'int32'},parse_dates=['date'],
    infer_datetime_format=True,
)
   PredictAndGraph(sum_sales_,choice_tienda)   
      

def TimeSeriesProductos():
   dict_dias = {1 : "Lunes", 2 : "Martes" , 3 : "Miercoles" , 4 : "Jueves" , 5 : "Viernes" , 6 : "Sabado" , 7 : "Domingo"}
   
   family_sales = pd.read_csv("productos.csv")
   productos = family_sales.family.tolist()

   choice_producto = st.selectbox("Elige el producto",\
    ["Todos los productos"] + productos)

   
   if choice_producto != "Todos los productos":
      sum_sales_ = pd.read_csv("sales_by_date_and_family_and_promotion.csv",usecols=['date','family', 'onpromotion','sales'],
                              dtype={'family': 'str','onpromotion' : 'int32',
      'sales': 'float32',},parse_dates=['date'],
    infer_datetime_format=True).set_index("family").loc[choice_producto]
   else:
      sum_sales_ = pd.read_csv("sales_by_date_and_promotion.csv",
                              usecols=['date','onpromotion', 'sales'],
                              dtype={'sales': 'float32','onpromotion':'int32'},parse_dates=['date'],
    infer_datetime_format=True,
)
   PredictAndGraph(sum_sales_,choice_producto)       


def TimeSeriesCiudades():
   dict_dias = {1 : "Lunes", 2 : "Martes" , 3 : "Miercoles" , 4 : "Jueves" , 5 : "Viernes" , 6 : "Sabado" , 7 : "Domingo"}
   
   ciudades = pd.read_csv("cities.csv")
   ciudades = ciudades.city.tolist()
   choice_ciudad = st.selectbox("Elige la ciudad",\
    ["Todas las ciudades"] + ciudades)

   
   if choice_ciudad != "Todas las ciudades":
      sum_sales_ = pd.read_csv("sales_by_date_and_cities_and_promotion.csv",usecols=['date','city', 'onpromotion','sales'],
                              dtype={'city': 'str','onpromotion' : 'int32',
      'sales': 'float32',},parse_dates=['date'],
    infer_datetime_format=True).set_index("city").loc[choice_ciudad]
   else:
      sum_sales_ = pd.read_csv("sales_by_date_and_promotion.csv",
                              usecols=['date','onpromotion', 'sales'],
                              dtype={'sales': 'float32','onpromotion':'int32'},parse_dates=['date'],
    infer_datetime_format=True,
)
   PredictAndGraph(sum_sales_,choice_ciudad)