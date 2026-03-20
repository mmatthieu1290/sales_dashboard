import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from toExcel import downloadExcel

def graph_years(responses,df):
   
   years = df.year.tolist()
   years = [str(year) for year in years]
   por_ciudades = False
   por_tiendas = False
   por_tipo_de_productos = False

   if "ciudades" in responses:

       por_ciudades = True
       options_ciudades = responses["ciudades"]
       options_ciudades.sort()    

   if "ciudades_productos" in responses:

      por_ciudades = True
      por_tipo_de_productos = True
      options_ciudades_productos = responses["ciudades_productos"]
      options_ciudades_productos.sort()    

   if "tiendas" in responses:

       por_tiendas = True
       options_tiendas = responses["tiendas"]
       numeros_tiendas = [int(store.split(" ")[1]) for store in options_tiendas]
       numeros_tiendas.sort()
       options_tiendas = ["Store" + " " + str(numero_tienda) for numero_tienda in numeros_tiendas]
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
       options_productos.sort()
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]
       options_tiendas_productos_num = [(int(elt[0].split(" ")[1]),elt[1]) for elt in options_tiendas_productos]
       options_tiendas_productos_num.sort()
       options_tiendas_productos = [("Store " + str(elt[0]),elt[1]) for elt in options_tiendas_productos_num]


   if por_ciudades:
       
      if por_tipo_de_productos == False:
           
         df_toexcel = pd.DataFrame(columns = ['year','sales','ciudad'])
         fig = go.Figure()
         for ciudad in options_ciudades:
            df_ciudad = df[df.city == ciudad]
            df_ciudad_year = df_ciudad.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
            sales = df_ciudad_year.sales.tolist()            
            df_ciudad_year["ciudad"] = ciudad
            df_toexcel = pd.concat([df_toexcel,df_ciudad_year])
            fig.add_trace(go.Scatter(x=years,y=sales,name=str(ciudad),mode = "lines+markers",marker=dict(size=8)))
         df_toexcel = df_toexcel[['ciudad','year','sales']].sort_values(["ciudad","year"])
         downloadExcel(df_toexcel.rename(columns={"ciudad":"city"}),"resultados_por_año_ciudad.xlsx")

      else:
         df_toexcel = pd.DataFrame(columns = ['year','sales','ciudad','producto'])
         fig = go.Figure()
         for ciudad_producto in options_ciudades_productos:
            ciudad,producto = ciudad_producto
            df_ciudad_producto = df[(df.family == producto)&(df.city == ciudad)]
            df_ciudad_producto_year = df_ciudad_producto.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
            sales = df_ciudad_producto_year.sales.tolist()            
            df_ciudad_producto_year["ciudad"] = ciudad
            df_ciudad_producto_year["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_ciudad_producto_year])
            fig.add_trace(go.Scatter(x=years,y=sales,name=ciudad + " " +str(producto),mode = "lines+markers",marker=dict(size=8)))
         df_toexcel = df_toexcel[["ciudad",'producto','year','sales']]
         df_toexcel = df_toexcel.sort_values(["ciudad","producto","year"])
         downloadExcel(df_toexcel.rename(columns={"ciudad":"city","producto":"product"}),"resultados_por_año_ciudad_producto.xlsx")                                         

      fig.update_xaxes(title_text = "year",title_font = {"size": 20},
        title_standoff = 25,ticktext=years,tickvals=years,)
      fig.update_yaxes(title_text = "sells",title_font = {"size": 20},
        title_standoff = 25)
      st.plotly_chart(fig, config = {'scrollZoom': False}) 

   else:
      if (por_tiendas == False) and (por_tipo_de_productos == False):
         df_year = df.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
         sales = df_year.sales.tolist()
         fig = go.Figure()
         fig.add_trace(go.Scatter(x=years,y=sales,mode = "lines+markers",marker=dict(size=8)))
         downloadExcel(df_year,"resultados_por_año.xlsx")


      elif por_tipo_de_productos == False:
         df_toexcel = pd.DataFrame(columns = ['year','sales','tienda'])
         fig = go.Figure()
         for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df[df.store_nbr == nb_store]
            df_store_year = df_store.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
#            years = df_store_year.year.tolist()
            sales = df_store_year.sales.tolist()            
            fig.add_trace(go.Scatter(x=years,y=sales,name=str(store),mode = "lines+markers",marker=dict(size=8)))
            df_store_year['tienda'] = store
            df_toexcel = pd.concat([df_toexcel,df_store_year])
         df_toexcel = df_toexcel[['tienda','year','sales']].sort_values(["tienda","year"])
         downloadExcel(df_toexcel.rename(columns={"tienda":"store"}),"resultados_por_año_tienda.xlsx")
      elif por_tiendas == False:
         df_toexcel = pd.DataFrame(columns = ['year','sales','producto'])
         fig = go.Figure()
         for producto in options_productos:
            df_producto = df[df.family == producto]
            df_producto_year = df_producto.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
            sales = df_producto_year.sales.tolist()            
            df_producto_year["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_producto_year])
            fig.add_trace(go.Scatter(x=years,y=sales,name=str(producto),mode = "lines+markers",marker=dict(size=8)))
         df_toexcel = df_toexcel[['producto','year','sales']].sort_values(["producto","year"])
         downloadExcel(df_toexcel.rename(columns={"producto":"product"}),"resultados_por_año_producto.xlsx")       
      else:
         df_toexcel = pd.DataFrame(columns = ['year','sales','tienda','producto'])
         fig = go.Figure()
         for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df[(df.family == producto)&(df.store_nbr == nb_tienda)]
            df_tienda_producto_year = df_tienda_producto.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
            sales = df_tienda_producto_year.sales.tolist()            
            df_tienda_producto_year["tienda"] = tienda
            df_tienda_producto_year["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_tienda_producto_year])
            fig.add_trace(go.Scatter(x=years,y=sales,name=tienda + " " +str(producto),mode = "lines+markers",marker=dict(size=8)))
         df_toexcel = df_toexcel[["tienda",'producto','year','sales']]
         df_toexcel = df_toexcel.sort_values(["tienda","producto","year"])
         downloadExcel(df_toexcel.rename(columns={"tienda":"store","producto":"product"}),"resultados_por_año_tienda_producto.xlsx")       
      fig.update_xaxes(title_text = "year",title_font = {"size": 20},
        title_standoff = 25,ticktext=years,tickvals=years,)
      fig.update_yaxes(title_text = "sells",title_font = {"size": 20},
        title_standoff = 25)
      st.plotly_chart(fig, config = {'scrollZoom': False})   

