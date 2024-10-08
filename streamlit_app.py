import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import io
import tempfile

from functions import *

# The page title, shown in the browser tab
st.set_page_config(page_title= "CPT Merger by PSZ")

#----------------------------------------------
# CPT DATA IMPORT
st.header("CPT DATA IMPORT")

uploaded_files = st.file_uploader("Upload Excel files (.xls, .xlsx)",
                                  type= ['xls', 'xlsx'],
                                  accept_multiple_files=True)

# H.abs DYNAMIC INPUT TABLE
# Extract file names of uploaded files
files = [file.name for file in uploaded_files]  # read filenames
file_names = [(f.split(".")[0]) for f in files] # split and get first part of filename

# Create DataFrame
H_default_values = (np.full(shape=(len(file_names)), fill_value=100.01)).tolist()

df = (pd.DataFrame([file_names, H_default_values],
                   index=['CPT FILE NAME','Ground Level [mBf]'])).transpose()

# Create data editor
edited_df = st.data_editor(df, num_rows="dynamic")

#-------------------------------------------------
sheet_type = st.radio("Import data from sheet as", options=['Sheet Number', 'Sheet Name'],
                      index= 0,
                      help = "Decides if the number (int) or the name (string) of the sheet will be defined.")

col1, col2 = st.columns(2)

with col1:
    if sheet_type == "Sheet Number":
        sheet_ID = st.number_input("Sheet Number (0: automatically get data from first sheet)", 
                                   value = 0, step=1)
    else:
        sheet_ID = st.text_input("Sheet name", value = 'Munka1')
    col_data = st.text_input("Columns - z [m], qc [MPa], Rf [%]", 
                             value="A, B, H",
                             help= "Define the column ID's where z, qc, Rf data is located.")

with col2:
    header_row = st.number_input("Header data row", min_value= 1, step= 1,
                                 help= "Row number containing the column headers in the Excel file")
    data_startrow = st.number_input("Number of rows from header where data starts", min_value= 1, value= 1, step= 1,
                                    help= "Row with 'z = 0.00' starting data, after header row")

# Excel import to Pandas DatFrames
@st.cache_data
def file_import_to_pandas(upl_files, sh_ID, h_row, startrow, data_cols):
    df = [] #empty container

    for uploaded_file in upl_files:
        read_df = pd.read_excel(uploaded_file,
                                sheet_name= sh_ID,
                                header = h_row-1,
                                skiprows = startrow-1,
                                usecols= data_cols,
                                names= ['z', 'qc', 'Rf'])
        df.append(read_df)

    return df

dataframes = file_import_to_pandas(uploaded_files,
                                   sheet_ID,
                                   header_row,
                                   data_startrow,
                                   col_data)

# 'z' column conversion to absolute height, new SBT index column
for i in range(len(dataframes)):
    dataframes[i]['z'] = edited_df.iloc[i][1] - dataframes[i]['z']
    dataframes[i]['SBT'] = SBT(qc= dataframes[i]['qc'],
                               Rf= dataframes[i]['Rf'])

#-----------------------------------------------------
# PLOTTING
st.divider()
st.header("PLOT")

col1, col2 = st.columns(2)

with col1:
    xaxis_data = st.selectbox("Data on X-axis",
                            options=['qc', 'Rf', 'SBT'],
                            help= "Select the preferred column from qc, Rf or SBT index.")
    if xaxis_data == 'qc':
        x_max_value = st.slider("Maximum value on X axis", max_value= 100, value=30, step=5)
    elif xaxis_data == 'Rf':
        x_max_value = st.slider("Maximum value on X axis", max_value= 10, value=6)
    else:
        x_max_value = st.slider("Maximum value on X axis", max_value= 8, value=4)

with col2:
    plot_width = st.slider("Diagram width (px)", min_value=100, max_value=1000, value=600, step=50)
    plot_height = st.slider("Diagram height (px)", min_value=100, max_value=2000, value=800, step=50)


fig = plotly_lineplot(dfs= dataframes,
                      x_data= xaxis_data,
                      x_max= x_max_value,
                      df_cptnames= edited_df,
                      d_width= plot_width,
                      d_height= plot_height)

st.plotly_chart(fig, use_container_width=False)


# Project Name
project_ID = st.text_input("Project name", value="Sample project",
                           help= "Name of the project")

#---------------------------------------------------------------
# DOWNLOAD IMAGE AS PDF, PNG OR HTML FILE
dcol1, dcol2, dcol3 = st.columns(3, gap='small')

with dcol1:
    # Save the figure to a PNG buffer
    png_buffer = io.BytesIO()
    fig.write_image(png_buffer, format='png', scale=2, engine='kaleido')

    # Reset the buffer position to the beginning
    png_buffer.seek(0)

    # Add a button to download the figure as a PDF
    st.download_button(label="Download as PNG",
                       data=png_buffer,
                       file_name= project_ID + "_merged CPT data_"+ xaxis_data +".png")

with dcol2:
    # Save the figure to a PDF buffer
    pdf_buffer = io.BytesIO()
    fig.write_image(pdf_buffer, format='pdf', scale=2, engine='kaleido')

    # Reset the buffer position to the beginning
    pdf_buffer.seek(0)

    # Add a button to download the figure as a PDF
    st.download_button(label="Download as PDF",
                       data=pdf_buffer,
                       file_name= project_ID + "_merged CPT data_"+ xaxis_data +".pdf")

with dcol3:
    # Save the figure as an HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        fig.write_html(tmp.name)
        tmp.seek(0)
        html_data = tmp.read()

    # Add a button to download the figure as an HTML file
    st.download_button(
        label="Download as HTML",
        data=html_data,
        file_name= project_ID + "_merged CPT data_"+ xaxis_data +".html",
        mime="text/html"
    )


#-------------------------------------------------------
# TABLE RESULTS
expander = st.expander("View Table Results", expanded=False)
if len(files) > 0:
    df_name = expander.selectbox("Select Table", options= file_names, index= 0)
    expander.write(dataframes[file_names.index(df_name)])
else:
    expander.markdown("No files uploaded yet!")