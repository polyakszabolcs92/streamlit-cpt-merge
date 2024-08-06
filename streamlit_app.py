import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import io

from functions import *

#----------------------------------------------
st.title("CPT DATA MERGER")

# CPT DATA IMPORT
st.header("CPT DATA IMPORT")
uploaded_files = st.file_uploader("Upload Excel files (.xls, .xlsx)",
                               type= ['xls', 'xlsx'],
                               accept_multiple_files=True)

# H.abs DYNAMIC INPUT TABLE
# Extract file names of uploaded files
file_names = [file.name for file in uploaded_files]

# Create DataFrame
H_default_values = (np.full(shape=(len(file_names)), fill_value=100.01)).tolist()
df = (pd.DataFrame([file_names, H_default_values],
                   index=['CPT FILE ID','Ground Level [mBf]'])).transpose()

# Create data editor
edited_df = st.data_editor(df, num_rows="dynamic")

#-------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    sheet_ID = st.text_input("Sheet ID", value = None)
    header_row = st.number_input("Header data row #", min_value= 1, step= 1,
                                 help= "Row number containig the column headers in the Excel file")
    data_startrow = st.number_input("Data start row", min_value= 2, value= 2, step= 1,
                                    help= "Row with z = 0.00 [m] data")

with col2:
    col_data = st.text_input("Columns - z [m], qc [MPa], Rf [%]", 
                             value="A, B, C")

# 
dataframes = []
for uploaded_file in uploaded_files:
    read_df = pd.read_excel(uploaded_file,
                            sheet_name= 0,
                            header = header_row-1,
                            skiprows = data_startrow-2,
                            usecols= col_data,
                            names= ['z', 'qc', 'Rf'])
    dataframes.append(read_df)

# 'z [m]' oszlop relatívból abszolút magasság, és új SBT index oszlop
for i in range(len(dataframes)):
    dataframes[i]['z'] = edited_df.iloc[i][1] - dataframes[i]['z']
    dataframes[i]['SBT'] = SBT(qc= dataframes[i]['qc'],
                               Rf= dataframes[i]['Rf'])



# PLOTTING
st.divider()
xaxis_data = st.selectbox("Data on X-axis",
                          options=['qc', 'Rf', 'SBT'])

if xaxis_data == 'qc':
    x_max_value = st.slider("Maximum value on X axis", max_value= 100, value=30)
elif xaxis_data == 'Rf':
    x_max_value = st.slider("Maximum value on X axis", max_value= 10, value=5)
else:
    x_max_value = st.slider("Maximum value on X axis", max_value= 6, value=4)


fig = plotly_lineplot(dfs=dataframes,
                      x_data= xaxis_data,
                      x_max=x_max_value,
                      df_cptnames= edited_df,
                      d_width=800,
                      d_height=800)

st.plotly_chart(fig)
