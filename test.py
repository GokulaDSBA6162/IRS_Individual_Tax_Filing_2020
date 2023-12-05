import streamlit as st
import numpy as np
import pandas as pd
import pip

pip.main(["install", "openpyxl"])

df = pd.read_csv('20incyall - 1024 - Project.csv')

st.write('IRS Data')

st.dataframe(df)
  
st.write('Trying to plot the map')

st.map(df,
    latitude='Latitude',
    longitude='Longitude'
    )
