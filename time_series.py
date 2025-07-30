import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess
import pickle

def TimeSeries():
 
   store_sales = pd.read_csv(
     'store_sales_2017.csv',
    usecols=['store_nbr', 'date', 'sales'],
    dtype={
        'store_nbr': 'category',
        'sales': 'float32',
    },
    parse_dates=['date'],
    infer_datetime_format=True,
)
   store_sales["store_nbr"] = store_sales.store_nbr.astype(int)
   tiendas = [f"Tienda {nb_store}" for nb_store in store_sales.sort_values("store_nbr").store_nbr.unique()]
   choice_tienda = st.selectbox("Elige la tienda",\
    ["Todas las tiendas"] + tiendas)
   store_sales['date'] = store_sales.date.dt.to_period('D')

   
   if choice_tienda != "Todas las tiendas":
      nb_tienda = int(choice_tienda.split(" ")[1])
      store_sales = store_sales[store_sales.store_nbr == nb_tienda]
      file_name = "_".join(choice_tienda.split(" "))+"LR.pkl"
      with open('Tiendas_LR/'+file_name,'rb') as LR:
         lr = pickle.load(LR)
   else:
      with open('Tiendas_LR/all_LR.pkl','rb') as LR:
         lr = pickle.load(LR)          


   store_sales = store_sales.set_index(['store_nbr',  'date']).sort_index()
   sum_sales = (
    store_sales
    .groupby('date').sum()
    .squeeze()
    .loc['2017']
)
   y_past = sum_sales.copy()
   fourier = CalendarFourier(freq="M", order=4) 
   dp = DeterministicProcess(
    index=y_past.index,
    constant=True,
    order=1,
    seasonal=True,
    additional_terms=[fourier],
    drop=True,
)
   X_past = dp.in_sample()


   X_future = dp.out_of_sample(steps=(pd.Period('2017-12-31') - y_past.index[-1]).n + 1)
   y_pred_future = pd.Series(lr.predict(X_future).reshape((-1)), index=X_future.index)
   fig = go.Figure()
   fig.add_trace(go.Scatter(x=y_past.index.astype(str),y=y_past,mode = "lines+markers",marker=dict(size=8),name="Past"))
   fig.add_trace(go.Scatter(x=y_pred_future.index.astype(str),y=y_pred_future,mode = "lines+markers",marker=dict(size=8),\
             name="Prediction"))
   fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Ventas")
   st.plotly_chart(fig, config = {'scrollZoom': False})                  