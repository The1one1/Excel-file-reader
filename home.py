import streamlit as st 
import pandas as pd
import plotly.express as px
import base64  # standard library
from io import StringIO, BytesIO   # standard library
import xlsxwriter


st.set_page_config(page_title='Home', page_icon=':bar_chart:',
                     layout='wide', initial_sidebar_state='auto')
st.header('Excel file to Graph :📈:')



def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, encoding='utf-8', index=False, header=True) # write to buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="GroupBy_data.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)
 

# --Upload Excel File--
uploded_file = st.file_uploader('Upload Excel File', type = 'xlsx')

if uploded_file:
    st.markdown('---')
    file = pd.read_excel(uploded_file, engine = 'openpyxl')
    st.dataframe(file)
    
    groupBy_columns = st.selectbox('Select GroupBy', options = file.columns, index = 0)
    
    intrested_columns = ['Sales', 'Profit']
    groupBy_df = file.groupby(groupBy_columns, as_index=False)[intrested_columns].sum()
    
    st.dataframe(groupBy_df)
    
    
    # --Plot--
    
    fig = px.bar(
        groupBy_df,
        x = groupBy_columns,
        y = 'Sales',
        color= 'Profit',
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Sale and Profit by {groupBy_columns}</b>' 
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    
    # --Download --
    # st.download_button(
    #     label = 'Download Excel File as CSV File',
    #     data=groupBy_df.to_csv(index=False),
    #     file_name='GroupBy_data.csv',
    #     mime = 'text/csv'
    # )
    
    # --Download Excel File--
    generate_excel_download_link(groupBy_df)