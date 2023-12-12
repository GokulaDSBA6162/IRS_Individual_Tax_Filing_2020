import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import altair as alt

#set the required titles

APP_TITLE = "IRS INDIVIDUAL TAX FILING - 2020"
APP_SUB_TITLE = "STATEWISE/COUNTYWISE INCOME"

st.set_page_config(APP_TITLE, layout="wide")
st.title(APP_TITLE)
st.markdown(
    "*This section presents the following facts based on the chosen State and/or County:*\n"
)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# #Load IRS Data
# pip.main(["install", "openpyxl"])
# df = pd.read_csv('data/20incyall - 1024 - STProject.csv')

@st.cache
def load_data(url):
    df = pd.read_csv(url)
    return df

# Assuming you have a CSV file locally
df = load_data('data/20incyall - 1024 - STProject.csv')

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

#Filter the data based on State and County

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

#Calculate the Tax Income facts
single = filtered_df["Number of single returns"].sum()
joint = filtered_df["Number of joint returns"].sum()
hh = filtered_df["Number of head of household returns"].sum()
total_income = int(filtered_df["Total income in Amount"].sum())
total_returns = filtered_df["Total income in Number of returns"].sum()
percent_single =  ((filtered_df["Number of single returns"].sum() /
                    filtered_df['Total income in Number of returns'].sum()) * 100)
percent_j =  ((filtered_df["Number of joint returns"].sum() /
                    filtered_df['Total income in Number of returns'].sum()) * 100)
percent_h =  ((filtered_df["Number of head of household returns"].sum() /
                    filtered_df['Total income in Number of returns'].sum()) * 100)

#Display settings
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.write("Total Returns:")
    st.write(f"{total_returns:,}")
with col2:
    st.write("Total Income:")
    st.write(f"US $ {total_income:,}")
with col3:
    st.write("Single Returns:")
    st.write(f"{single:,}")
    st.write(f"{percent_single:,.2f}%")
with col4:
    st.write("Joint Returns:")
    st.write(f"{joint:,}")
    st.write(f"{percent_j:,.2f}%")
with col5:
    st.write("HOH Returns:")
    st.write(f"{hh:,}")
    st.write(f"{percent_j:,.2f}%")

#tab1,tab2 = st.tabs(["STATEWISE TAX INCOME DATA", "COMPARE INCOME TAX FACTS"])

# tab1, tab2 = st.tabs(["STATEWISE TAX INCOME DATA", "COMPARE INCOME TAX FACTS"])
# with tab1:

#     #Code to display map
#     st.markdown(
#     "***In this view, users of this application can explore visualizations for the selected states to understand which states generate higher tax income. The map highlights the highest tax-paying states in darker colors and the least tax-paying states in lighter colors. The bar charts default to displaying the Top 10 and Bottom 10 states in terms of Individual Income Tax of 2020. When a multi-select state filter is applied, it shows the Top and Bottom states based on the selection.***\n"
#     )

#     state_agg= filtered_df.groupby(['StateName', 'State'], as_index=False).aggregate({'Number of single returns':'sum','Number of joint returns':'sum','Number of head of household returns':'sum', 'Total income in Amount':'sum'})

#     map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
   
#     choropleth = folium.Choropleth(
#         geo_data='data/us-state-boundaries.geojson',
#         data=state_agg,
#         columns=('State', 'Total income in Amount'),
#         key_on='feature.properties.stusab',
#         line_opacity=0.8,
#         highlight=True
#     )
#     choropleth.geojson.add_to(map)

#     choropleth.geojson.add_child(
#         folium.features.GeoJsonTooltip(['name'],labels=False)
#     )

#     st_map = st_folium(map, width=1400, height=700)
    
#     #Code to display chart of Top 10

#     fact_df= filtered_df.groupby(['StateName', 'State'], as_index=False).aggregate({'Number of single returns':'sum','Number of joint returns':'sum','Number of head of household returns':'sum', 'Total income in Amount':'sum'})

#     st.subheader("Top 10 Highest Tax Paying States")
#     # Create a rank column based on total income
#     fact_df['Rank'] = fact_df['Total income in Amount'].rank(ascending=False)

#     # Filter the data to include only the top 10 ranks
#     top_10_df = fact_df[fact_df['Rank'] <= 10]

#     # Create the Altair chart
#     freq_chart = alt.Chart(top_10_df).mark_bar().encode(
#         y=alt.Y('StateName:N', title="State", sort=alt.EncodingSortField('Total income in Amount', op='min', order='descending')),
#         x=alt.X('Total income in Amount:Q', axis=alt.Axis(grid=False)),
#     ).properties(
#         height=400,
#         width=800
#     )

#     freq_text = freq_chart.mark_text(
#         align='left',
#         baseline='middle',
#         dx=3
#     ).encode(
#         text=alt.Text('Total income in Amount:Q', format='.0f')
#     ).properties(
#         height=400,
#         width=800
#     )

#     # Display the chart
#     (freq_chart + freq_text)

#     #Code to display chart of lowest 10

#     st.subheader("Lowest Tax Paying States")
#     # Create a rank column based on total income
#     fact_df['Rank'] = fact_df['Total income in Amount'].rank(ascending=True)

#     # Filter the data to include only the bottom 10 ranks
#     bottom_10_df = fact_df[fact_df['Rank'] <= 10]

#     # Create the Altair chart
#     freq_chart = alt.Chart(bottom_10_df).mark_bar().encode(
#         y=alt.Y('StateName:N', title="State", sort=alt.EncodingSortField('Total income in Amount', op='min', order='ascending')),
#         x=alt.X('Total income in Amount:Q', axis=alt.Axis(grid=False)),
#     ).properties(
#         height=400,
#         width=800
#     )

#     freq_text = freq_chart.mark_text(
#         align='left',
#         baseline='middle',
#         dx=3
#     ).encode(
#         text=alt.Text('Total income in Amount:Q', format='.0f')
#     ).properties(
#         height=400,
#         width=800
#     )

#     # Display the chart
#     (freq_chart + freq_text)

# # with tab2:
    
    tab2_state_agg= filtered_df.groupby(['StateName'], as_index=False).aggregate({'Number of single returns':'sum','Number of joint returns':'sum',
                                                                                      'Number of head of household returns':'sum', 
                                                                                      'Total income in Amount':'sum',
                                                                                      'Total income in Number of returns':'sum',
                                                                                      'Number of  farm returns':'sum',
                                                                                      'Total itemized deductions in Number of returns':'sum',
                                                                                      'Residential energy tax credit in Number of returns':'sum'})
    tab2_state_agg.rename(columns={'Residential energy tax credit in Number of returns': 'Residential energy tax credit'}, inplace=True)
    tab2_state_agg2= filtered_df.groupby(['StateName', 'County name'], as_index=False).aggregate({'Number of single returns':'sum','Number of joint returns':'sum',
                                                                                    'Number of head of household returns':'sum', 
                                                                                    'Total income in Amount':'sum',
                                                                                    'Total income in Number of returns':'sum',
                                                                                    'Number of  farm returns':'sum',
                                                                                    'Total itemized deductions in Number of returns':'sum',
                                                                                    'Residential energy tax credit in Number of returns':'sum'})
    tab2_state_agg2.rename(columns={'Residential energy tax credit in Number of returns': 'Residential energy tax credit'}, inplace=True)

    
    st.header("Select a State and/or County from the sidebar to compare the facts on the scatterplot.")

    st.markdown(
    "*This view empowers users to select and compare states, exploring various tax statistics. The comparison feature allows users to understand the standing of different states and counties based on the chosen tax factor. For instance, users interested in discovering which state received Residential Energy Tax Credits in 2022 can make that selection to gather relevant insights.*\n"
    )

    st.markdown(
    "***Note: While all tax facts provide information about returns, only 'Total Income' reflects the corresponding dollar amounts.***\n"
)   

    x_val = st.selectbox("Pick your x-axis fact",tab2_state_agg2.columns.drop(['StateName','County name']).tolist())
    y_val = st.selectbox("Pick your y-axis fact",tab2_state_agg2.columns.drop(['StateName','County name']).tolist())

    if not county:
        scatter = alt.Chart(tab2_state_agg, title=f"{x_val} and {y_val}").mark_point().encode(
        alt.X(x_val,title=f'{x_val}'),
        alt.Y(y_val,title=f'{y_val}'),
        tooltip=['StateName','Total income in Amount',x_val, y_val], size = 'Total income in Amount').configure_mark(
        opacity=0.5,
        color='blue')
        st.altair_chart(scatter, theme="streamlit", use_container_width=True)
    else:
        scatter = alt.Chart(tab2_state_agg2, title=f"{x_val} and {y_val}").mark_point().encode(
        alt.X(x_val,title=f'{x_val}'),
        alt.Y(y_val,title=f'{y_val}'),
        tooltip=['StateName','County name','Total income in Amount',x_val, y_val], size = 'Total income in Amount').configure_mark(
        opacity=0.5,
        color='StateName')
        st.altair_chart(scatter, theme="streamlit", use_container_width=True)

    st.dataframe(tab2_state_agg2)

