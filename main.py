# import necessary packages
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


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

# # headers and texts
# st.title("Data Report")

# col1, col2 = st.columns([50,50])

# with col1:
with st.container(height=400):
    # for the map visualization
    location = data[["neighborhood_group","lat", "long"]]
    location = location.dropna()
    st.map(location, latitude="lat", longitude="long")

# with col2:
with st.container(height=400):
    # for the donut chart visualization
    policy = data.groupby("cancellation_policy").agg({"cancellation_policy":"size"}).to_dict()
    policy = pd.DataFrame(policy).reset_index()
    policy = policy.rename(columns={"index": "cancellation_policy", "cancellation_policy":"no_of_hosts"})

    policy = go.Figure(data=[go.Pie(values=policy["no_of_hosts"], hole=0.3, textinfo='label+percent')])
    st.plotly_chart(policy)

# print(data.head(100))
# print(data.columns) 


# st.line_chart(x=)


