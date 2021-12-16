#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 14:04:02 2021

@author: christiansaintlouis
"""

import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
import time






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
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)

st.subheader('Pivot Table Capturing the Rating for All Hospitals Using the Parameters of Hospital Ownership and Hospital Type')
dataframe_pivot = df_hospital_2.pivot_table(index=['hospital_ownership','hospital_type'],values=['hospital_overall_rating'],aggfunc='count')
st.dataframe(dataframe_pivot)

hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']

hospitals_tx = df_hospital_2[df_hospital_2['state'] == 'TX']

#Bar Chart
st.subheader('Hospital Type in New York')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.caption('Most of the hospitals in the New York area are acute care, followed by psychiatric')


st.subheader('Visual Representation:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)
st.caption('The pie chart above shows the different hospital types in the New York Area, with 75.4% being acute care hospitals')



st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)

st.subheader('Hospital Type in New York')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.caption('Most of the hospitals in the New York area are acute care, followed by psychiatric')


st.subheader('Visual Representation:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)
st.caption('The pie chart above shows the different hospital types in the New York Area, with 75.4% being acute care hospitals')



#Timeliness of Care
st.subheader('NY Hospitals - Timeliness of Care')
bar2 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.caption('Based on the above bar chart, we can see the majority of hospitals in the NY area fall below the national\
        average as it relates to timeliness of care')


st.subheader('TX Hospitals - Timeliness of Care')
bar4 = hospitals_tx['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig5 = px.bar(bar4, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig5)
st.caption('Based on the bar chart above, we can see the the timeliness of care data for the majority of hospitals in the Texas area is not available and for 127 hospitals is the same as the national average')


st.markdown('Hospital Q1: What is the most common hospital type in NY & and where do NY hospitals fall in regards to timeliness of care?')
st.markdown('As shown by the analysis above, the most common hospital type in NY is acute care (144 acute care hospitals). Most of New York Hospitals are below national average in regards to timeliness of care(103 hospitals)') 

#Drill down into INPATIENT and OUTPATIENT 
st.title('INPATIENT dataframe')
st.markdown('The dataframe displayed below is for the Inpatient facility')

st.subheader('Inpatient Facility')
bar7 = df_inpatient_2['provider_state'].value_counts().reset_index()
st.dataframe(bar7)

st.subheader('Bar Chart of Inpatient Facilities by state')
fig7 = px.bar(bar7, x='index', y='provider_state')
st.plotly_chart(fig7)



inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.subheader('Discharges')
st.markdown('Total Count of Discharges from Inpatient Captured: ' )
st.markdown( str(total_inpatient_count) )

common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()

st.markdown('The dataframe displayed below is for the outpatient facility')

st.subheader('Outpatient Facility')
bar7 = df_outpatient_2['provider_state'].value_counts().reset_index()
st.dataframe(bar7)

st.subheader('Bar Chart of outpatient Facilities by state')
fig7 = px.bar(bar7, x='index', y='provider_state')
st.plotly_chart(fig7)

st.markdown('Q2.  Which states have the greatest number of inpatient and outpatient facilities?')
st.markdown('- As shown by the analysis above, Florida has the most inpatient facilities and Texas has the most outpatient facilities') 

top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.subheader('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.columns(2)

col1.subheader('Top 10 DRGs')
col1.dataframe(top10)

col2.subheader('Bottom 10 DRGs')
col2.dataframe(bottom10)

st.markdown('Q3. What is Stony Brooks top three and bottom three inpatient DRG service?')
st.markdown('- As shown by the analysis above, the top 3 are heart transplant, ecmo, and t rach\
                while the bottom 3 are trauma related, hiv related conditions') 


st.header('Merging datasets for SBU and CEMC Hopsital values')
st.markdown('Merging of Datasets to show SBU Hospital values')
df_hospital_2['provider_id'] = df_hospital_2['provider_id'].astype(str)
df_outpatient_2['provider_id'] = df_outpatient_2['provider_id'].astype(str)
df_merged = df_outpatient_2.merge(df_hospital_2, how='left', left_on='provider_id', right_on='provider_id')

st.dataframe(df_merged)
st.markdown('Cleaning of df_merge')
df_merged_clean = df_merged[df_merged['hospital_name'].notna()]
st.dataframe(df_merged_clean)

st.header('Stony Brook University Hospital dataset')
df_merged_clean_SB = df_merged_clean[df_merged_clean['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
df_merged_clean_SB

st.header('Carolina East Medical Center')
df_merged_clean_CEMC = df_merged_clean[df_merged_clean['hospital_name'] == 'CAROLINA EAST MEDICAL CENTER']
df_merged_clean_CEMC

st.header('Comparison of CEMC and SBU Hospitals')
final_df_comparison = pd.concat([df_merged_clean_CEMC, df_merged_clean_SB])
st.dataframe(final_df_comparison)

st.subheader('Final Comparison Pivot Table')
dataframe_pivot = final_df_comparison.pivot_table(index=['hospital_name','apc'],values=['average_total_payments'],aggfunc='mean')
st.dataframe(dataframe_pivot)


























