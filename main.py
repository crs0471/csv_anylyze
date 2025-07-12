import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta

from streamlit_date_picker import date_range_picker, date_picker, PickerType
st.set_page_config(
    page_title="Data Visualization App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state = "collapsed"
)

# state init
st.session_state.df = pd.DataFrame()
st.session_state.header_list = []
st.session_state.line_chart_data = defaultdict(list)


st.subheader("Upload CSV | Visualize | Analyze")
def load_df():
    if not st.session_state.df.empty:
        st.session_state.header_list = [key for key, val in st.session_state.df.dtypes.to_dict().items() if val in ['int64', 'float64']]
        with st.expander("Data Info", expanded=True):
            info_tab, desc_tab = st.tabs(["Info", "Description"])
            with info_tab:
                st.write("Data Types")
                st.dataframe(st.session_state.df.dtypes, height=150)
                st.write("Shape")
                st.write(f"Total Rows : {st.session_state.df.shape[0]} | Total Columns : {st.session_state.df.shape[1]}")
            
            with desc_tab:
                st.write("Data Description")
                st.dataframe(st.session_state.df.describe(), height=150)

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload a Data File.", type=["csv",])
    if uploaded_file:
        df = pd.read_csv(uploaded_file, index_col=False)
        st.session_state.df = df

with col2:
    load_df()
        
# ================= edit section =====================

edit_section = st.expander("Edit Section", expanded=False)
with edit_section:
    st.subheader("Edit Data")
    st.session_state.df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True,
        key="edit_data",
    )


def create_bar():
    c1, c2 = st.columns([1,2])
    selected_x = c1.selectbox("Select Base Column", st.session_state.df.columns, key="bar_x")
    selected_y = c2.multiselect("Columns For Bar Chart", st.session_state.header_list, default=[], key="bar_y")
    if selected_x and selected_y:
        chart_data = st.session_state.df.groupby(selected_x)[selected_y].mean().reset_index()
        st.bar_chart(
            chart_data,
            x=selected_x,
            y=selected_y, height=250)
        
def create_line():
    c1, c2, c3 = st.columns([1,2,1])
    selected_x = c1.selectbox("Select Base Column", st.session_state.df.columns, key="line_x")
    selected_y = c2.multiselect("Columns For Bar Chart", st.session_state.header_list, default=[], key="line_y")
    if selected_x:
        with c3:
            try:
                st.session_state.df['date_obj'] = pd.to_datetime(st.session_state.df[selected_x]).dt.date
                if len(st.session_state.df['date_obj'].unique().tolist()) <= 1:
                    raise Exception("Date column has only one unique value")
                start_x = st.session_state.df['date_obj'].min()
                end_x = st.session_state.df['date_obj'].max()
                ic1, ic2 = st.columns(2)
                x_filter_start = ic1.date_input("Select Start Date", value=start_x, key="line_x_filter")
                x_filter_end = ic2.date_input("Select End Date", value=end_x, key="line_x_filter_end")
                st.session_state.df = st.session_state.df[(st.session_state.df['date_obj'] >= x_filter_start) & (st.session_state.df['date_obj'] <= x_filter_end)]
                st.session_state.df = st.session_state.df.drop(columns=['date_obj'])
            except Exception as e:
                values = st.session_state.df[selected_x].unique()
                values.sort()
                selected = c3.multiselect("Select values for filter", values, default=values[-5:], key="line_x_date",)
                st.session_state.df = st.session_state.df[st.session_state.df[selected_x].isin(selected)]
    if selected_x and selected_y:
        chart_data = st.session_state.df.groupby(selected_x)[selected_y].mean().reset_index()
        st.line_chart(
            chart_data,
            x=selected_x,
            y=selected_y, height=250)
        

with st.container(border=True):
    st.subheader("Analyze | Visualize | Predict")

    tab_bar, tab_line = st.tabs(["Bar Chart", "Line Chart"])

    with tab_bar:
        create_bar()

    with tab_line:
        create_line()


with st.sidebar:
    st.subheader("Data Analysis")
    st.write("This is a simple data visualization app that allows you to upload a CSV file and visualize the data using bar and line charts.")
    st.write("You can select the columns you want to visualize and the app will generate the charts for you.")
    st.write("This app is built using Streamlit, a Python library for building web apps.")
    st.write("You can use this app to quickly visualize your data and gain insights from it.")
    st.write(" Relex We are not storing any data.")




