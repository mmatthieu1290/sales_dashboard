import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def first_page(connexion):
    
    # Cargar datos
   #sales_by_date = pd.read_csv("sales_by_date.csv", parse_dates=["date"],
   #                            infer_datetime_format=True)
   sales_by_date = pd.read_sql_query('select * from sales_by_date' \
    , con = connexion)
   sales_by_date['date'] = sales_by_date['date'].apply(lambda x : datetime.strptime(x , "%Y-%m-%d"))
   sales_by_date['date'] = sales_by_date.date.dt.to_period('D')
   sales_by_date = sales_by_date.sort_values("date")
#   sales_by_store = pd.read_csv("sales_by_store.csv")
   sales_by_store = pd.read_sql_query('select * from sales_by_store' \
    , con = connexion)
#   sales_by_family = pd.read_csv("sales_by_family.csv")
   sales_by_family = pd.read_sql_query('select * from sales_by_family' \
    , con = connexion)   

   # Sección 1: Evolución de ventas en el tiempo
   st.header("Evolución de ventas en el tiempo")
   # fig, ax = plt.subplots()
   # ax.plot(sales_by_date["date"], sales_by_date["sales"], label="Ventas diarias")
   # ax.set_xlabel("Fecha")
   # ax.set_ylabel("Ventas")
   # ax.set_title("Ventas totales por día")
   # st.pyplot(fig)

   fig = go.Figure()
   fig.add_trace(go.Scatter(x=sales_by_date["date"].astype(str),y = sales_by_date["sales"],
                            mode = "lines+markers",marker=dict(size=8)))
   fig.update_layout(
      title=dict(
        text="Ventas totales por día"
    ) ,
      xaxis_title="Fecha",
      yaxis_title="Ventas")    

   st.plotly_chart(fig, config = {'scrollZoom': False}) 

   # Sección 2: Ventas por tienda
   st.header("Ventas por tienda")
   st.bar_chart(data=sales_by_store, x="store_nbr", y="sales")

   # Sección 3: Ventas por familia de productos
   st.header("Ventas por familia de productos")
   top_families = sales_by_family.head(15)
   st.bar_chart(data=top_families, x="family", y="sales")

def first_questions(por_ciudad,por_tiendas,por_tipo_de_productos,df):

    responses = {}

    if por_ciudad:
       
       if por_tipo_de_productos:
          opt = df[["city","family"]].value_counts().to_frame().reset_index()[["city","family"]].sort_values(["city","family"]).values
          opt = [(f"{elt[0]}",elt[1]) for elt in opt]
          options_ciudad_productos = st.multiselect(
       "Qué ciudad y productos quieres analizar",
        default=[],
        options=opt
        )    
          responses.update({"ciudades_productos":options_ciudad_productos})
       else:
           options_ciudad = st.multiselect(
       "Qué ciudades quieres analizar?",
        default=[],
        options=list(df.sort_values("city").city.unique())
        )  
           responses.update({"ciudades":options_ciudad})                        


    else:
       if por_tiendas and por_tipo_de_productos == False:
          opt = [f"Tienda {tienda_city}" for tienda_city in df.sort_values("store_nbr").store_nbr_city.astype(str).unique()]
          options_tiendas = st.multiselect(
       "Qué tiendas quieres analizar",
        default=[],
        options=opt
        )
          responses.update({"tiendas":options_tiendas}) 

       if por_tipo_de_productos and por_tiendas == False:
          options_productos = st.multiselect(
          "Qué tipo de productos quieres analizar",
           default=[],
           options=list(df.sort_values("family").family.unique())
           )  
          responses.update({"productos":options_productos})     
       if por_tiendas and por_tipo_de_productos:
          opt = df[["store_nbr","family"]].value_counts().to_frame().reset_index()[["store_nbr","family"]].sort_values(["store_nbr","family"]).values
          opt = [(f"Tienda {elt[0]}",elt[1]) for elt in opt]
          options_tiendas_productos = st.multiselect(
          "Qué tiendas y productos quieres analizar",
           default=[],
           options=opt
           )    
          responses.update({"tiendas_productos":options_tiendas_productos})

    return responses

