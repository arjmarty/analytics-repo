# import necessary packages
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os

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
                                      "review rate number": "review_rating", 
                                      "calculated host listings count": "listings_count",
                                      "availability 365": "annual_availability"})


st.set_page_config(layout="wide")

# main header/ title
st.header("Airbnb Data Report", divider="blue")

# Wrap your content inside a div with this class
css_path = os.path.expanduser("~/analytics-repo/analytics-repo/styles.css")
print(css_path)
with open(css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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
with st.container(height=600, border=True, key="viz1-container"):
    col1, col2, col3 = st.columns([30,35,35], gap="medium", border=True)
    with col1:
        st.markdown("**Map Visualization of Airbnb Listing Locations**")
        # for the map visualization
        location = data[["neighborhood_group","lat", "long"]]
        location = location.dropna()
        st.map(location, latitude="lat", longitude="long", size=20)

    with col2:
        # for the bar chart visualization of neighborhood groups breakdown
        # data cleaning on string fields
        data["neighborhood_group"] = data["neighborhood_group"].dropna().str.replace("brookln","Brooklyn").str.replace("manhatan", "Manhattan")
        #group by according to no. of airbnb hosts per neighborhood group
        loc_group = data.groupby("neighborhood_group").agg({"neighborhood_group":"size"}).to_dict()
        loc_group = pd.DataFrame(loc_group).reset_index()
        loc_group = loc_group.rename(columns={"index":"neighborhood_group", "neighborhood_group": "no_of_hosts"})
        st.markdown("**Airbnb Hosts Neighborhood Group**")
        # since st.bar_chart has limited feature (especially on data inside bar labels, I will use)
        loc_group_bar = px.bar(loc_group, x="neighborhood_group", y="no_of_hosts", text_auto=True)
        loc_group_bar.update_traces(marker=dict(color="steelblue"))
        loc_group_bar.update_xaxes(title="Neighborhood Group", showline=True, linecolor='gray')
        loc_group_bar.update_yaxes(title="No. of Hosts", showline=True, linecolor='gray')
        st.plotly_chart(loc_group_bar)
        # st.bar_chart(data=loc_group, x="neighborhood_group", y="no_of_hosts", x_label="Neighborhood Group", y_label="Number of Hosts") 
        # -- this can also be used in case you want from streamlit direct

    with col3:
        st.markdown("**Airbnb Room Types Breakdown**")
        room_type = data.groupby("room_type").agg({"room_type":"size"}).to_dict()
        room_type = pd.DataFrame(room_type).reset_index()
        room_type = room_type.rename(columns={"index":"room_type", "room_type":"no_of_hosts"})
        room_type_donut = go.Figure(data=[go.Pie(values=room_type["no_of_hosts"], labels=room_type["room_type"], hole=0.4, textinfo='label+percent')])
        st.plotly_chart(room_type_donut)

with st.container(height=None, border=True):
    col1, col2 = st.columns([40, 60], gap="large", border=True)
    with col1:
        st.markdown("**Host Cancellation Policy Breakdown**")
        # for the donut chart visualization
        colors = ["olive", "darksalmon", "mediumslateblue"]
        policy = data.groupby("cancellation_policy").agg({"cancellation_policy":"size"}).to_dict()
        policy = pd.DataFrame(policy).reset_index()
        policy = policy.rename(columns={"index": "cancellation_policy", "cancellation_policy":"no_of_hosts"})
        policy = go.Figure(data=[go.Pie(values=policy["no_of_hosts"], labels=policy["cancellation_policy"], hole=0.4, textinfo='label+percent')])
        policy.update_traces(marker=dict(colors=colors))
        st.plotly_chart(policy)
    
    with col2:
        st.markdown("**Airbnb Listing Breakdown by Construction Year**")
        cons_year = data.groupby("construction_year").agg({"construction_year":"size"}).to_dict()
        cons_year = pd.DataFrame(cons_year).reset_index()
        cons_year = cons_year.rename(columns={"index": "construction_year", "construction_year":"no_of_hosts"})
        cons_year_line = px.line(cons_year, x="construction_year", y="no_of_hosts", text="no_of_hosts")
        cons_year_line.update_traces(textposition="bottom right")
        cons_year_line.update_xaxes(title="Construction Year", showline=True, linecolor='gray')
        cons_year_line.update_yaxes(range=[0, 5500], title="No. of Hosts", showline=True, linecolor='gray')
        st.plotly_chart(cons_year_line)



with st.container(height=None, border=True):
    col1, col2, col3 = st.columns([28,36,36], gap="large", border=True)
    with col1:
        st.markdown("**Top NY Airbnb Hosts (by Reviews)**")
        #cleaned the no. of reviews by replacing "NA" with 0
        data["number_of_reviews"] = data["number_of_reviews"].fillna(0).astype(int)
        top_host = data[["host_name","number_of_reviews"]].round({"number_of_reviews":0}).sort_values(by="number_of_reviews", ascending=False)
        top_host["number_of_reviews"] = top_host["number_of_reviews"]
        top_host["host_name"] = top_host["host_name"].replace("M", "Unknown Host")
        top_host = top_host.rename(columns={"host_name": "Host Name", "number_of_reviews": "No. of Reviews"})
        top_host = top_host.head(10).reset_index(drop=True)
        top_host.index = top_host.index + 1
        st.table(top_host)

    with col2:
        rating = data.groupby("review_rating").agg({"review_rating":"size"}).to_dict()
        rating = pd.DataFrame(rating).reset_index()
        rating = rating.rename(columns={"index": "review_rating", "review_rating":"no_of_hosts"})
        st.markdown("**Airbnb Hosts Breakdown by Review Ratings**")
        review_ratings = px.bar(rating, x="no_of_hosts", y="review_rating", text_auto=True, orientation='h', labels={"no_of_hosts": "No. of Hosts", "review_rating": "Review Rating"})
        review_ratings.update_traces(marker=dict(color="teal"))
        st.plotly_chart(review_ratings)
        
    with col3:
        st.markdown("**Top NY Airbnb Hosts with Five-Star Ratings**")
        data["review_rating"] = data["review_rating"].fillna(0).astype(int).round(0)
        top_host2 = data[["host_name","number_of_reviews", "review_rating"]].sort_values(by=["review_rating", "number_of_reviews"], ascending=False)
        top_host2 = top_host2.drop_duplicates().head(10).reset_index(drop=True)
        top_host2 = top_host2.rename(columns={"host_name":"Host Name", "number_of_reviews": "No. of Reviews", "review_rating": "Rating"})
        top_host2.index = top_host2.index + 1
        st.table(top_host2)


#Overall overview of the data for analyses: uncomment from time to time to uncover more insights
# pd.set_option('display.max_columns', None)
# print(data)
# print(data.columns) 




