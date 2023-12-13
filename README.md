# dsba_5122_final_project


# Streamlit App Link
https://irsindividualtaxfiling2020.streamlit.app/

# Introduction:
Analyzing statewise IRS individual tax returns data can provide useful insights and solutions for various issues. Here are some potential problems that can be addressed using IRS individual tax returns data. Please be aware that the dataset contains all the necessary data points to underpin the following analysis, even though you may not observe many of them in the Streamlit app. In the app, I brought in very few features for the project's objectives.

Comparative Analysis of States: Enable users to compare tax data among different states to make informed decisions about where to live or conduct business. Highlight states with lower tax burdens or favorable tax environments.

Retirement Planning by State: Provide insights into how state tax policies can impact retirement planning. Analyze states with favorable conditions for retirees, considering factors such as pension taxation and Social Security benefits.

Education on State Tax Credits: Educate individuals about state-specific tax credits and incentives. This could include credits for education, homeownership, energy efficiency, and other state-supported initiatives.

Impact of Local Taxes: Consider the impact of local taxes (city or county) in addition to state taxes. Provide a comprehensive view of the overall tax burden at different geographical levels.

State Economic Trends: Analyze statewise tax data to identify economic trends and patterns. This information can be useful for individuals considering job opportunities, investments, or business ventures.

Decision Support for Entrepreneurs: For entrepreneurs and small business owners, analyze state tax data to provide insights into business-related taxes, credits, and deductions. Support decision-making related to business location and operations.

# Data Preparation and Design Implementation:
The data required for this project is collected from this site - https://www.irs.gov/statistics/soi-tax-stats-county-data-2020. The raw data required very few data cleanup like:

-Converting the datatypes from object to int or float or string as required.
-Converted the State name abbreviations into State Names

The dataset contain no missing data or invalid data.

For the map visualization, I used the geopy.geocoders module to get the latitude and longitude based on the county names. And added those values in the dataset. But I did not use the latitude and longitude values to plot the map instead i used Folium library to create choropleth map. 

For the purpose of this project, I have focused on a select set of data points as highlighted below. However, it's important to note that the dataset contains a wealth of additional information that can be leveraged to address a broader range of inquiries and objectives.

Referenced the following streamlit apps to create mine:
https://www.youtube.com/watch?v=uXj76K9Lnqc

https://github.com/liammaxwell24/dsba_5122_final_project

Some designs from here: https://www.youtube.com/watch?v=7yAw1nPareM&t=113s

Some with the help of ChatGPT.


# Future Work:

Analyzing tax-related data geographically through maps can uncover regional variations and trends. In future improvements, I aim to enhance map interactivity, although my attempts in this regard were unsuccessful this time.

Explore and integrate more variables from the dataset to gain valuable insights. This may encompass factors such as deductions, credits, or specific sources of income.

Create visualizations illustrating trends over time. This involves scrutinizing alterations in income, deductions, or tax credits over various years or periods.
