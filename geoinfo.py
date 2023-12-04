import streamlit as st
import time
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import pip

pip.main(["install", "openpyxl"])

df = pd.read_csv('20incyall - 1024 - Project.csv')

st.dataframe(df)


unique_cities = df['Address'].unique()
print("Number of unique cities:", len(unique_cities))

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="city_locator")

city_data = []

for city in unique_cities:
    location = geolocator.geocode(city, timeout=None)
    if location is not None:
        print(city, location.latitude, location.longitude)
        city_data.append({
            'County': city,
            #'State': location.state,
            'Latitude': location.latitude,
            'Longitude': location.longitude
        })

city_df = pd.DataFrame(city_data)
city_df.to_csv('city_coordinates.csv', index=False)

st.dataframe(city_df)