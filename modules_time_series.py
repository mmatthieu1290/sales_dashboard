import pandas as pd
import streamlit as st
from datetime import timedelta
import plotly.graph_objects as go
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX


def PredictAndGraph(sum_sales_,text_title):
   
   dict_dias = {1 : "Lunes", 2 : "Martes" , 3 : "Miercoles" , 4 : "Jueves" , 5 : "Viernes" , 6 : "Sabado" , 7 : "Domingo"}

   sum_sales_['date'] = sum_sales_.date.dt.to_period('D')
   min_date_considerated = sum_sales_.date.max() - timedelta(days = 365)
   sum_sales = sum_sales_[sum_sales_.date >= min_date_considerated]
   sum_sales = sum_sales.set_index("date")
   sum_sales_ = sum_sales_.set_index("date") 

   y_past = sum_sales.sales.copy()
   y_past_plot = sum_sales_.sales.copy()
   fourier = CalendarFourier(freq="M", order=4) 
   dp = DeterministicProcess(index=y_past.index,
    constant=True,
    order=1,
    seasonal=True,
    additional_terms=[fourier],
    drop=True,
)
   X_past = dp.in_sample()
   X_past['onpromotion'] = sum_sales['onpromotion']
   model = LinearRegression().fit(X_past, y_past)
   residuals = y_past - model.predict(X_past)
   

# Ajustamos un modelo SARIMAX(1,2,1) sobre los residuos
   sarimax_model = SARIMAX(residuals, order=(7, 1, 4))
   sarimax_fit = sarimax_model.fit(disp=False)

   date_range_past = st.date_input(
    "Selecciona desde que fecha quieres observar las ventas pasadas",
    value=y_past.index.max().to_timestamp()  - timedelta(days = 30),
    max_value = y_past.index.max().to_timestamp(), 
    min_value = y_past_plot.index.min().to_timestamp()
)   
   

   date_range_future = st.date_input(
    "Selecciona un intervalo de fechas para la prediccion futura",
    value=(y_past.index.max().to_timestamp() + timedelta(days = 1), y_past.index.max().to_timestamp() + timedelta(days = 30)),
    min_value = y_past.index.max().to_timestamp() + timedelta(days = 1)
)
   fig = go.Figure()
   # Predicción in-sample
   if isinstance(date_range_future, tuple) and len(date_range_future) == 2:

      residuals_prediction_one_more_month = sarimax_fit.predict(start = y_past.index.max().to_timestamp() + timedelta(days = 1),\
                                                             end = date_range_future[1])
      X_future = dp.out_of_sample(steps = (residuals_prediction_one_more_month.index[-1]\
                                     -y_past.index.max()).n+1)
      for date in X_future.index:
         X_future.loc[date,"onpromotion"] = X_past.loc[date - timedelta(days=365),'onpromotion']

      y_future  = pd.Series(model.predict(X_future).reshape((-1)), index=X_future.index)
      y_pred_future = y_future + residuals_prediction_one_more_month

      y_pred_future.loc[y_past.index.max()] = float(y_past.loc[y_past.index.max()])

      y_pred_future = y_pred_future.sort_index()
      y_pred_future_plot = y_pred_future.loc[[date.to_timestamp().date() >= date_range_future[0] for date in y_pred_future.index]]
      if date_range_future[0] == y_past.index.max().to_timestamp().date() + timedelta(days = 1):
         y_pred_future_plot.loc[y_past.index.max()] = float(y_past.loc[y_past.index.max()])

      y_pred_future_plot = y_pred_future_plot.sort_index()   

      y_past_plot = y_past_plot.loc[[(date.to_timestamp().date() >= date_range_past) for date in y_past_plot.index]]
      fig.add_trace(go.Scatter(x = y_past_plot.index.astype(str),y = y_past_plot.astype(float).values,\
                         mode = "lines+markers",marker=dict(size=8),name="Observado"))
      #fig.add_trace(go.Scatter(x=y_pred_future_plot.index.astype(str),y = y_pred_future_plot.astype(float).values,mode = "lines+markers",marker=dict(size=8),\
      #       name="Prediccion"))
      fig.add_trace(go.Scatter(x=y_pred_future_plot.index.astype(str),y = y_pred_future_plot.astype(float).values,mode = "lines+markers",marker=dict(size=8),\
             name="Prediccion"))      
      fig.update_layout(
      title=dict(
        text=text_title
    ) ,
      xaxis_title="Fecha",
      yaxis_title="Ventas")
      st.plotly_chart(fig, config = {'scrollZoom': False})        
      y_pred_future_plot = y_pred_future_plot.to_frame()
      y_pred_future_plot.columns = ["Ventas"]
      y_pred_future_plot["Dia"] = [date.day_of_week + 1 for date in y_pred_future_plot.index]
      y_pred_future_plot["Dia"] = y_pred_future_plot["Dia"].replace(dict_dias)
      st.dataframe(y_pred_future_plot)                    