#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 14:04:02 2021

@author: christiansaintlouis
"""


import pandas as pd
import streamlit as st
import numpy as np
import time
import plotly.figure_factory as ff
import scipy




st.title('Streamlit Final Assignment')
st.write('chsaintlouis Dashboard!') 

@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2

# FAKE LOADER BAR TO STIMULATE LOADING    
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)
  

df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()


st.header('Hospital Dataframe:')
st.dataframe(df_hospital_2)

st.subheader('Hospital Type')
bar1 = df_hospital_2['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.subheader('Pie Chart of Hospital Type')
fig = ff.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)

st.subheader('Pivot Table Capturing the Rating for All Hospitals Using the Parameters of Hospital Ownership and Hospital Type')
dataframe_pivot = df_hospital_2.pivot_table(index=['hospital_ownership','hospital_type'],values=['hospital_overall_rating'],aggfunc='count')
st.dataframe(dataframe_pivot)

hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']

hospitals_tx = df_hospital_2[df_hospital_2['state'] == 'TX']

