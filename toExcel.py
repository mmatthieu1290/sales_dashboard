import streamlit as st
from io import BytesIO
import pandas as pd
import xlsxwriter

def downloadExcel(df,nombre_archivo):
      output = BytesIO()
      writer = pd.ExcelWriter(output, engine='xlsxwriter')
      df.to_excel(writer, index=False, sheet_name='Sheet1')
      workbook = writer.book
      worksheet = writer.sheets['Sheet1']
      format1 = workbook.add_format({'num_format': '0.00'}) 
      worksheet.set_column('A:A', None, format1)  
      writer.close()
      processed_data = output.getvalue()
      st.download_button(label='📥 Download the results',
                                data=processed_data ,
                                file_name= nombre_archivo)