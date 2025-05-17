import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

#reading the data from excel file
df = pd.read_excel("AISolutions.xlsx")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('pic.PNG')

col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image,width=100)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px
    }
    </style>
    <center><h1 class="title-test">AI Solutions Dashboard</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")

with col4:
    fig = px.bar(df, x = "Product Sold", y = "Sales", labels={"Sales" : "Sales {$}"},
                 title = "Most Selling Product", hover_data={"Sales"},
                 template="gridon",height=500)
    st.plotly_chart(fig,use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns ([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Total Product Sales")
    data = df[["Product Sold", "Sales"]].groupby(by="Product Sold")["Sales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
                       file_name="Most Selling Product.csv", mime="text/csv")

df["Month_Year"] = df["DateTime"].dt.strftime("%b'%y")
result = df.groupby(by = df["Month_Year"])["Sales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x = "Month_Year", y = "Sales", title = "Product Sales Over Time",
                   template="gridon")
    st.plotly_chart(fig1,use_container_width=True)

with view2:
    expander = st.expander("Monthly Product Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("Get Data", data = result.to_csv().encode("utf-8"),
                       file_name="Monthly Product Sales.csv",mime="text/csv")

st.divider()

# Filter for job placements
job_placements = df[df["URIStem"].str.startswith("/jobs/placed/")]

# Count the number of job placements per country
jobs_by_country = job_placements.groupby("Country").size().reset_index(name="Jobs Placed")

fig2 = px.bar(jobs_by_country, x="Country", y="Jobs Placed", title="Number of Jobs Placed by Country", labels={"Jobs Placed": "Number of Jobs"},
    template="gridon",
    height=500,
    text_auto=True  # Display the number on top of each bar
)
# Customize hover information
fig2.update_traces(
    hovertemplate="<b>%{x}</b><br>Jobs Placed: %{y}<extra></extra>"
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

_, col6 =st.columns([0.1,1])
treemap = df[["UserAgent", "Country", "Sales"]].groupby(by = ["UserAgent","Country"])["Sales"].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{:.2f}'
    
treemap["Sales (Formatted)"] = treemap["Sales"].apply(format_sales)
fig4 = px.treemap(treemap,path = ["UserAgent","Country"], values = "Sales",
                  hover_data = ["Sales (Formatted)"],
                  color = "Country", height = 700, width = 600)
fig4.update_traces(textinfo="label+value")

with col6:
    st.subheader("Total Sales by User Agent and Country in treemap")
    st.plotly_chart(fig4,use_container_width=True)

_, view4, dwn4 = st.columns([0.5,0.45,0.45])
with view4:
    result2 = df[["UserAgent", "Country", "Sales"]].groupby(by = ["UserAgent","Country"])["Sales"].sum()
    expander = st.expander("View data for Total Sales by User Agent and Country")
    expander.write(result2)
with dwn4:
    st.download_button("Get Data", data = result2.to_csv().encode("utf-8"),
                                        file_name="Sales by User Agent.csv", mime="text.csv")
    
st.divider()


#If everything is wrong you can erase the whole part after this

df["Month_Year"] = df["DateTime"].dt.strftime("%b '%y")
monthly_sales = df.groupby("Month_Year")["Sales"].sum().reset_index()

# Sort the months chronologically
monthly_sales["Month_Year"] = pd.to_datetime(monthly_sales["Month_Year"], format="%b '%y")
monthly_sales = monthly_sales.sort_values("Month_Year")
monthly_sales["Month_Year"] = monthly_sales["Month_Year"].dt.strftime("%b '%y")

# Create a month selector
selected_month = st.selectbox("Select Month", monthly_sales["Month_Year"])

# Find the index of the selected month
selected_index = monthly_sales[monthly_sales["Month_Year"] == selected_month].index[0]

# Calculate current and previous sales
current_sales = monthly_sales.loc[selected_index, "Sales"]
if selected_index > 0:
    previous_sales = monthly_sales.loc[selected_index - 1, "Sales"]
    delta = current_sales - previous_sales
    percent_change = (delta / previous_sales) * 100 if previous_sales != 0 else 0
else:
    previous_sales = 0
    delta = 0
    percent_change = 0

# Create the indicator chart
fig5 = go.Figure(go.Indicator(
    mode="number+delta",
    value=current_sales,
    number={'prefix': "$", 'valueformat': ',.0f'},
    delta={'position': "right", 'reference': previous_sales, 'relative': True, 'valueformat': '.1%'},
    title={"text": f"Sales Change: {selected_month}"}
))

# Integrate into Streamlit layout
col7, col8 = st.columns([0.1, 1])
with col8:
    st.subheader("Sales Percentage Increase and Decrease Over Time")
    st.plotly_chart(fig5, use_container_width=True)

st.divider()


# 1. Count different types of Job Requests
job_requests = df[df["Job Requests"] != "-"]
job_request_counts1 = job_requests['Job Requests'].value_counts().reset_index()
job_request_counts1.columns = ['Job Type', 'Count']

# 2. Count Schedule Demo Requests
demo_requests1 = df[df['URIStem'].str.startswith('/schedule-demo/')]
demo_request_counts1 = demo_requests1['URIStem'].value_counts().reset_index()
demo_request_counts1.columns = ['Demo Type', 'Count']

# 3. Count Promotional Event Requests
promo_requests1 = df[df['URIStem'].str.startswith('/promotional-events/')]
promo_request_counts1 = promo_requests1['URIStem'].value_counts().reset_index()
promo_request_counts1.columns = ['Promo Type', 'Count']

# 4. Count Virtual Assistant Requests
virtual_assist_requests1 = df[df['URIStem'].str.startswith('/virtual-assistant/')]
virtual_assist_request_counts1 = virtual_assist_requests1['URIStem'].value_counts().reset_index()
virtual_assist_request_counts1.columns = ['', 'Count']

# Create the charts for each request type
fig_job = px.bar(job_request_counts1, x='Job Type', y='Count',
                 title='Job Requests', template='gridon', height=400)
fig_demo = px.scatter(demo_request_counts1, x='Demo Type', y='Count', 
                      title='Schedule Demo Requests', template='gridon', height=400)
fig_promo = px.pie(promo_request_counts1, names='Promo Type', values='Count',
                        title='Promotional Event Requests', height=400)
fig_virtual = px.bar(virtual_assist_request_counts1, x='', y='Count',
                     title='Virtual Assistant Requests', template='gridon', height=400)

# Display the charts in a single row with borders
col9, col10, col11, col12 = st.columns(4, gap="small")

with col9:
    with st.container(border=True):
        st.plotly_chart(fig_job, use_container_width=True)

with col10:
    with st.container(border=True):
        st.plotly_chart(fig_demo, use_container_width=True)

with col11:
    with st.container(border=True):
        st.plotly_chart(fig_promo, use_container_width=True)

with col12:
    with st.container(border=True):
        st.plotly_chart(fig_virtual, use_container_width=True)

st.divider()


# Convert 'DateTime' to datetime
df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')

# Convert columns to numeric, coercing errors to NaN
df['Httpstatus'] = pd.to_numeric(df['Httpstatus'], errors='coerce')
df['Timetaken'] = pd.to_numeric(df['Timetaken'], errors='coerce')
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

df['Sales'] = df['Sales'].replace(0, np.nan)

# Compute summary statistics for numeric columns
summary_stats = df[['Httpstatus', 'Timetaken', 'Sales']].describe().transpose()

# Compute summary statistics for 'DateTime' column
datetime_stats = df['DateTime'].agg(['min', 'max']).to_frame().transpose()

#####################################
df.columns = df.columns.str.strip().str.lower()

# Convert the 'min' column to datetime
df['min'] = pd.to_datetime(df['min'], errors='coerce')

# Replace 0 in 'Sales' with NaN for accurate statistics
df['Sales'] = df['Sales'].replace(0, np.nan)

####################################
# Combine the statistics
summary_stats = pd.concat([summary_stats, datetime_stats])

# Format datetime statistics to remove excessive decimal points
for col in ['mean', 'min', '25%', '50%', '75%', 'max']:
    if col in summary_stats.columns:
        summary_stats[col] = summary_stats[col].apply(
            lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) and isinstance(x, pd.Timestamp) else x
        )

# Create a new column for summary statistics
col13, _ = st.columns([1, 0.1])  # Adjust the width as needed

with col13:
    st.markdown("**Summary Statistics for AI Solutions**")
    st.dataframe(summary_stats, use_container_width=True)


st.divider()
