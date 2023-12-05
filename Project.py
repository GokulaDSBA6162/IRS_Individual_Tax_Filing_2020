import streamlit as st
import numpy as np
import pandas as pd
import pip

APP_TITLE = "IRS INDIVIDUAL TAX FILING - 2020"
APP_SUB_TITLE = "STATEWISE INCOME"

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

#Load IRS Data
pip.main(["install", "openpyxl"])
df = pd.read_csv('20incyall - 1024 - Project.csv')

df = df[(df['State']) == ]



st.write(df.shape)
st.write(df.head())
st.write(df.columns)


st.map(df,
    latitude='Latitude',
    longitude='Longitude'
    )
#if__name__== "__main__":
#main()
