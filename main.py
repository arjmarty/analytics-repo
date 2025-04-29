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


st.set_page_config(layout="wide")

# # main header/ title
st.header("Airbnb Data Report", divider="blue")

#list of metrics or number displays of important information
with st.container(height=170, border=False):
    a, b, c, d, e = st.columns(5, border=True)
    no_of_hosts = data["host_id"].count()
    a.metric("Number of hosts", value=f"{no_of_hosts:,}", border=False)


    data["host_identity_verified"].dropna()
    verified = (data["host_identity_verified"] == "verified").sum()
    pct1 = ((verified / data["host_id"].count()).__round__(3))*100
    b.metric("Verified Hosts", value=f"{verified:,}", delta=None, border=False)
    # Display the delta separately without the arrow
    b.write(f'''**:green[{pct1}%]** of the total number of hosts''')

    
    instant = (data["instant_bookable"] == True).sum()
    pct2 = ((instant / data["host_id"].count()).__round__(3))*100
    c.metric("Instantly Bookable Hosts", value=f"{instant:,}", border=False)
    c.write(f'''**:green[{pct2}%]** of the total number of hosts''')


    #Data cleaning on hosts' price before aggregation. Prices are in object data type, so need to be int so that computations are possible   
    prices = pd.Series(data["price"])
    prices = prices.str.replace("$", "", regex=False).str.replace(",", "", regex=False).dropna()
    prices = prices.astype(int)
    prices_total = prices.sum()
    prices_mean = prices.mean().__round__(2)
    d.metric("Overall NY Airbnb Hosts Price", value=f"${prices_total:,}")
    d.write(f'''Average Airbnb Host Price: **:blue[${prices_mean:,}]**''')

    #Data cleaning on airbnb service fee before aggregation. Prices are in object data type, so need to be int so that computations are possible   
    svc_fee = pd.Series(data["service_fee"])
    svc_fee = svc_fee.str.replace("$", "", regex=False).str.replace(",", "", regex=False).dropna()
    svc_fee = svc_fee.astype(int)
    svc_fee_total = svc_fee.sum()
    svc_fee_mean = svc_fee.mean().__round__(2)
    e.metric("Total Airbnb Service Fee Collected", value=f"${svc_fee_total:,}")
    e.write(f'''Average Airbnb Service Fee: **:blue[${svc_fee_mean:,}]**''')


# for the second line of visualizations
col1, col2 = st.columns([60,40], gap="medium")

with col1:
    with st.container(height=None):
        st.markdown("**Map Visualization of Airbnb Hosts**")
        # for the map visualization
        location = data[["neighborhood_group","lat", "long"]]
        location = location.dropna()
        st.map(location, latitude="lat", longitude="long", size=20)

with col2:
    with st.container(height=None):
        st.markdown("**Host Cancellation Policy Breakdown**")
        # for the donut chart visualization
        colors = ["olive", "darksalmon", "mediumslateblue"]
        policy = data.groupby("cancellation_policy").agg({"cancellation_policy":"size"}).to_dict()
        policy = pd.DataFrame(policy).reset_index()
        policy = policy.rename(columns={"index": "cancellation_policy", "cancellation_policy":"no_of_hosts"})
        policy = go.Figure(data=[go.Pie(values=policy["no_of_hosts"], labels=policy["cancellation_policy"], hole=0.4, textinfo='label+percent')])
        policy.update_traces(marker=dict(colors=colors))
        st.plotly_chart(policy)

pd.set_option('display.max_columns', None)
print(data)
print(data.columns) 


# st.line_chart(x=)


