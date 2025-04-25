# import necessary packages
import pandas as pd
import streamlit as st
import plotly.express as px


extracted_data = pd.read_csv("~/analytics-repo/analytics-repo/data-files/Airbnb_Open_Data.csv", low_memory=False)


#renaming columns for consistent format
data = extracted_data.rename(columns={"NAME": "name", "host id": "host_id", 
                                      "host name": "host_name", 
                                      "neighbourhood group": "neighborhood_group", 
                                      "country code": "country_code", 
                                      "room type": "room_type",
                                      "Construction year": "construction_year",
                                      "service fee": "service_fee",
                                      "minimum nights": "minimum nights",
                                      "number of reviews" : "number_of_reviews",
                                      "last review": "last_review", 
                                      "reviews per month": "reviews_per_month",
                                      " review rate number": "review_rating", 
                                      "calculated host listings count": "listings_count",
                                      "availability 365": "annual_availability"})

pd.set_option('display.max_columns', None)

# for the map visualization
location = data[["neighborhood_group","lat", "long"]]
location = location.dropna()
st.map(location, latitude="lat", longitude="long")

# st.title("Airbnb Data Report")

# st.line_chart(x=)


# print(data.head(100))
# print(data.columns)  
# map = px.scatter_geo()