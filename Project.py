import streamlit as st
import numpy as np
import pandas as pd
import pip
import plotly.express as px
import folium
from streamlit_folium import st_folium
import altair as alt

APP_TITLE = "IRS INDIVIDUAL TAX FILING - 2020"
APP_SUB_TITLE = "STATEWISE/COUNTYWISE INCOME"

st.set_page_config(APP_TITLE, layout="wide")
st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

#Load IRS Data
pip.main(["install", "openpyxl"])
df = pd.read_csv('data/20incyall - 1024 - STProject.csv')

df.State = df.State.astype('string')

#Create Sidebar for State and County Selection

st.sidebar.header("Choose your filter:")
state = st.sidebar.multiselect("Selet the State", df["StateName"].unique())
if not state:
    df2 = df.copy()
else:
    df2 = df[df["StateName"].isin(state)]
county = st.sidebar.multiselect("Selet the County", df2["County name"].unique())
if not county:
    df3 = df2.copy()
else:
    df3 = df2[df2["County name"].isin(county)]

# #Filter the data based on State and County

if not state and not county:
    filtered_df = df
elif not county:
    filtered_df = df[df["StateName"].isin(state)]
elif not state:
    filtered_df = df[df["County name"].isin(county)]
elif state and county:
    filtered_df = df3[df["StateName"].isin(state)&df3["County name"].isin(county)]
elif county:
    filtered_df = df3[df3["County name"].isin(county)]
else:
    filtered_df = df3[df3["StateName"].isin(state)&df3["County name"].isin(county)]

# ranking_g= filtered_df.groupby(['State','County name'], as_index=False).aggregate({'Number of single returns':'sum','Number of joint returns':'sum','Number of head of household returns':'sum', 'Total income in Amount':'sum'})
# st.write(ranking_g)

single = filtered_df["Number of single returns"].sum()
joint = filtered_df["Number of joint returns"].sum()
hh = filtered_df["Number of head of household returns"].sum()
total_income = int(filtered_df["Total income in Amount"].sum())
total_returns = filtered_df["Total income in Number of returns"].sum()
#percent_single = 


col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.write("Total Returns:")
    st.write(f"US $ {total_returns:,}")
with col2:
    st.write("Total Income:")
    st.write(f"US $ {total_income:,}")
with col3:
    st.write("Single Returns:")
    st.write(f"US $ {single:,}")
with col4:
    st.write("Joint Returns:")
    st.write(f"US $ {joint:,}")
with col5:
    st.write("HOH Returns:")
    st.write(f"US $ {hh:,}")

state_agg= filtered_df.groupby(['StateName', 'State'], as_index=False).aggregate({'Number of single returns':'sum','Number of joint returns':'sum','Number of head of household returns':'sum', 'Total income in Amount':'sum'})

map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
choropleth = folium.Choropleth(
    geo_data='data/us-state-boundaries.geojson',
    data=state_agg,
    columns=('State', 'Total income in Amount'),
    key_on='feature.properties.stusab',
    line_opacity=0.8,
    highlight=True
)
choropleth.geojson.add_to(map)

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name'],labels=False)
)

st_map = st_folium(map, width=700, height=450)

fact_df= df.groupby(['StateName', 'State'], as_index=False).aggregate({'Number of single returns':'sum','Number of joint returns':'sum','Number of head of household returns':'sum', 'Total income in Amount':'sum'})

st.subheader("Top 10 Highest Tax Paying States")
freq_chart = alt.Chart(fact_df).mark_bar().transform_filter(
    alt.FieldGTEPredicate(field='Total income in Amount', gte= 370000000)
        ).encode(
            y=alt.Y('StateName',sort=alt.EncodingSortField('Total income in Amount', op='min', order='descending')),
            x='Total income in Amount'
        ).properties(
    height=400,
    width=800
)

freq_text = freq_chart.mark_text(
    align='left',
    baseline='middle',
    dx=3
).encode(
        text=alt.Text('Total income in Amount',format='.0f')
    ).properties(
    height=400,
    width=800
)
freq_chart + freq_text

st.subheader("Lowest Tax Paying States")
freq_chart = alt.Chart(fact_df).mark_bar().transform_filter(
    alt.FieldLTEPredicate(field='Total income in Amount', lte= 45000000)
        ).encode(
            y=alt.Y('StateName',sort=alt.EncodingSortField('Total income in Amount', op='min', order='ascending')),
            x='Total income in Amount'          
        ).properties(
    height=400,
    width=700
)

freq_text = freq_chart.mark_text(
    align='left',
    baseline='middle',
    dx=3
).encode(
    text=alt.Text('Total income in Amount',format='.0f')
).properties(
    height=400,
    width=700
)
(freq_chart + freq_text)


