import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# ===== USER AUTHENTICATION =====
def authenticate_user(username, password):
    """Authenticate users against the predefined credentials"""
    users = {
        "David001": {"password": "David2025", "name": "David"},
        "Sarah002": {"password": "Sarah2025", "name": "Sarah"},
        "Leonard003": {"password": "Leonard2025", "name": "Leonard"},
        "Mandy004": {"password": "Mandy2025", "name": "Mandy"}
    }
    
    if username in users and users[username]["password"] == password:
        return {"authenticated": True, "name": users[username]["name"]}
    return {"authenticated": False}


def login_page():
    """Display login form with dark blue theme"""
    # Set dark blue background with subtle gradient
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a192f 0%, #172a45 100%);
            height: 100vh;
        }
        .login-container {
            background-color: rgba(23, 42, 69, 0.8);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            width: 400px;
            margin: auto;
            margin-top: 5%;
        }
        .login-title {
            color: #64ffda;
            text-align: center;
            margin-bottom: 30px;
            font-size: 28px;
            font-weight: 600;
            letter-spacing: 1px;
        }
        .stTextInput>div>div>input {
            border-radius: 6px;
            padding: 12px 15px;
            background-color: rgba(10, 25, 47, 0.7);
            border: 1px solid rgba(100, 255, 218, 0.3);
            color: #ccd6f6;
        }
        .stTextInput>div>div>input::placeholder {
            color: rgba(204, 214, 246, 0.5);
        }
        .stButton>button {
            width: 100%;
            border-radius: 6px;
            padding: 12px;
            background: linear-gradient(135deg, #64ffda 0%, #0a192f 100%);
            color: #0a192f;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #64ffda 0%, #1e3b70 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(100, 255, 218, 0.3);
        }
        .error-message {
            text-align: center;
            color: #ff5555;
            margin-top: 15px;
            font-weight: 500;
            background-color: rgba(255, 85, 85, 0.1);
            padding: 8px;
            border-radius: 6px;
            border: 1px solid rgba(255, 85, 85, 0.3);
        }
        .success-message {
            text-align: center;
            color: #64ffda;
            margin-top: 15px;
            font-weight: 500;
            background-color: rgba(100, 255, 218, 0.1);
            padding: 8px;
            border-radius: 6px;
            border: 1px solid rgba(100, 255, 218, 0.3);
        }
        .logo-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .input-label {
            color: #64ffda;
            font-size: 14px;
            margin-bottom: 8px;
            display: block;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Check if user is already authenticated
    if st.session_state.get("authenticated"):
        st.markdown(
            """
            <div class="login-container">
                <h1 class="login-title">Welcome, {}</h1>
                <p class="success-message">Login Successful!</p>
            </div>
            """.format(st.session_state["user"]),
            unsafe_allow_html=True
        )
        return

    # Login form container
    st.markdown(
        """
        <div class="login-container">
            <div class="logo-container">
                <svg width="0" height="0" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" fill="#64ffda"/>
                    <path d="M12 6C8.69 6 6 8.69 6 12C6 15.31 8.69 18 12 18C15.31 18 18 15.31 18 12C18 8.69 15.31 6 12 6Z" fill="none" stroke="#0a192f" stroke-width="2"/>
                    <path d="M12 10C10.9 10 10 10.9 10 12C10 13.1 10.9 14 12 14C13.1 14 14 13.1 14 12C14 10.9 13.1 10 12 10Z" fill="#0a192f"/>
                </svg>
            </div>
            <h1 class="login-title">AI SOLUTIONS</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Login form
    with st.form("login_form"):
        st.markdown(
            """
            <style>
            .form-container {
                padding: 0 20px;
            }
            </style>
            <div class="form-container">
            """,
            unsafe_allow_html=True
        )
        
        st.markdown('<span class="input-label">Username</span>', unsafe_allow_html=True)
        username = st.text_input("", placeholder="Enter your username", label_visibility="collapsed")
        
        st.markdown('<span class="input-label">Password</span>', unsafe_allow_html=True)
        password = st.text_input("", type="password", placeholder="Enter your password", label_visibility="collapsed")
        
        submit_button = st.form_submit_button("LOGIN")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if submit_button:
            auth_result = authenticate_user(username, password)
            if auth_result["authenticated"]:
                st.session_state["authenticated"] = True
                st.session_state["user"] = auth_result["name"]
                st.rerun()  # This will reload the page and show the success message
            else:
                st.markdown(
                    '<p class="error-message">Username or password incorrect</p>',
                    unsafe_allow_html=True
                )


# ===== MAIN DASHBOARD =====
def main_dashboard():
    # Set page config - must be first Streamlit command
    st.set_page_config(layout="wide")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    
    # ===== DATA LOADING =====
    @st.cache_data(ttl=3600)  # Cache expires after 1 hour
    def load_data():
        df = pd.read_excel("AISolutions.xlsx")
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        return df
    
    df = load_data()
    image = Image.open('pic.PNG')

    # ===== SIDEBAR =====
    with st.sidebar:
        # Create columns for image and title
        col_img, col_title = st.columns([1, 3])
        
        with col_img:
            try:
                st.image(image, width=80)
            except Exception as e:
                st.error(f"Could not load image: {e}")
        
        with col_title:
            st.markdown("""
            <style>
            .sidebar-title {
                font-weight: bold;
                font-size: 18px;
                text-align: left;
                margin: 10px 0;
                color: #1f77b4;
                padding-top: 15px;
            }
            </style>
            <div class="sidebar-title">AI Solutions Dashboard</div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")        
        
        # Display user info and logout button at top
        st.markdown(f"**Logged in as:** {st.session_state['user']}")
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.rerun()
        
        st.markdown("---")
                
        # Navigation header
        st.markdown("**Dashboard Tabs**")
        selected_tab = st.radio(
            "Go to:",
            ["Sales Overview", "Visuals by Country", "More Visuals", "Traffic Analysis"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Filters header
        st.header("Filter Data")
        
        # Product filter
        products = ['All'] + sorted(df['Product Sold'].unique().tolist())
        selected_product = st.selectbox('Select Product', products)
        
        # Country filter
        countries = ['All'] + sorted(df['Country'].unique().tolist())
        selected_country = st.selectbox('Select Country', countries)
        
        # Date range filter
        min_date = df['DateTime'].min().date()
        max_date = df['DateTime'].max().date()
        start_date, end_date = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Last updated info
        st.markdown("---")
        box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
        st.caption(f"Last updated: {box_date}")

    # Apply filters to the dataframe
    filtered_df = df.copy()
    if selected_product != 'All':
        filtered_df = filtered_df[filtered_df['Product Sold'] == selected_product]
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['Country'] == selected_country]
    filtered_df = filtered_df[
        (filtered_df['DateTime'].dt.date >= start_date) & 
        (filtered_df['DateTime'].dt.date <= end_date)
    ]

    # ===== TAB CONTENT =====
    if selected_tab == "Sales Overview":
        # Create two columns for the first two charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(filtered_df, x="Product Sold", y="Sales", labels={"Sales": "Sales {$}"},
                         title="Most Selling Product", hover_data={"Sales"},
                         template="gridon", height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table for Most Selling Product
            expander = st.expander("Total Product Sales")
            data = filtered_df[["Product Sold", "Sales"]].groupby(by="Product Sold")["Sales"].sum()
            expander.write(data)
        
        with col2:
            # Create monthly sales data
            filtered_df["Month_Year"] = filtered_df["DateTime"].dt.strftime("%b'%y")
            result = filtered_df.groupby(by=filtered_df["Month_Year"])["Sales"].sum().reset_index()
            
            fig1 = px.line(result, x="Month_Year", y="Sales", title="Product Sales Over Time",
                           template="gridon", height=400)
            st.plotly_chart(fig1, use_container_width=True)
            
            # Data table for Monthly Sales
            expander = st.expander("Monthly Product Sales")
            expander.write(result)
        
        # Summary Statistics section
        st.subheader("Summary Statistics for AI Solutions")
        
        # Convert columns to numeric, coercing errors to NaN
        filtered_df['Httpstatus'] = pd.to_numeric(filtered_df['Httpstatus'], errors='coerce')
        filtered_df['Timetaken'] = pd.to_numeric(filtered_df['Timetaken'], errors='coerce')
        filtered_df['Sales'] = pd.to_numeric(filtered_df['Sales'], errors='coerce')
        
        # Replace 0 in 'Sales' with NaN for accurate statistics
        filtered_df['Sales'].replace(0, np.nan, inplace=True)
        
        # Compute summary statistics for numeric columns
        summary_stats = filtered_df[['Httpstatus', 'Timetaken', 'Sales']].describe().transpose()
        
        # Compute summary statistics for 'DateTime' column
        datetime_stats = filtered_df['DateTime'].agg(['min', 'max']).to_frame().transpose()
        
        # Combine the statistics
        summary_stats = pd.concat([summary_stats, datetime_stats])
        
        # Format datetime statistics
        for col in ['mean', 'min', '25%', '50%', '75%', 'max']:
            if col in summary_stats.columns:
                summary_stats[col] = summary_stats[col].apply(
                    lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) and isinstance(x, pd.Timestamp) else x
                )
        
        # Display the summary statistics
        st.dataframe(summary_stats, use_container_width=True)

    elif selected_tab == "Visuals by Country":
        # Jobs by country chart
        job_placements = filtered_df[filtered_df["URIStem"].str.startswith("/jobs/placed/")]
        
        if not job_placements.empty:
            jobs_by_country = job_placements.groupby("Country").size().reset_index(name="Jobs Placed")
            
            fig2 = px.bar(jobs_by_country, x="Country", y="Jobs Placed", 
                         title="Number of Jobs Placed by Country", 
                         labels={"Jobs Placed": "Number of Jobs"},
                         template="gridon",
                         height=400,
                         text_auto=True)
            fig2.update_traces(
                hovertemplate="<b>%{x}</b><br>Jobs Placed: %{y}<extra></extra>"
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Data table for Jobs by Country
            expander = st.expander("View Jobs by Country Data")
            expander.write(jobs_by_country)
        else:
            st.warning("No job placement data available with current filters")
        
        # Treemap of sales by user agent and country
        st.subheader("Total Sales by User Agent and Country")
        
        treemap = filtered_df[["UserAgent", "Country", "Sales"]].groupby(by=["UserAgent","Country"])["Sales"].sum().reset_index()
        
        def format_sales(value):
            if value >= 0:
                return '{:.2f}'.format(value)
        
        treemap["Sales (Formatted)"] = treemap["Sales"].apply(format_sales)
        fig4 = px.treemap(treemap, path=["UserAgent","Country"], values="Sales",
                          hover_data=["Sales (Formatted)"],
                          color="Country", height=500)
        fig4.update_traces(textinfo="label+value")
        st.plotly_chart(fig4, use_container_width=True)
        
        # Data table for Treemap
        result2 = filtered_df[["UserAgent", "Country", "Sales"]].groupby(by=["UserAgent","Country"])["Sales"].sum()
        expander = st.expander("View data for Total Sales by User Agent and Country")
        expander.write(result2)

    elif selected_tab == "More Visuals":
        # Sales percentage change indicator
        st.subheader("Sales Percentage Increase and Decrease Over Time")
        
        filtered_df["Month_Year"] = filtered_df["DateTime"].dt.strftime("%b '%y")
        monthly_sales = filtered_df.groupby("Month_Year")["Sales"].sum().reset_index()
        
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
        
        st.plotly_chart(fig5, use_container_width=True)
        
        # Request type charts in columns
        col3, col4, col5, col6 = st.columns(4)
        
        with col3:
            # Job Requests
            job_requests = filtered_df[filtered_df["Job Requests"] != "-"]
            if not job_requests.empty:
                job_request_counts = job_requests['Job Requests'].value_counts().reset_index()
                job_request_counts.columns = ['Job Type', 'Count']
                
                fig_job = px.bar(job_request_counts, x='Job Type', y='Count',
                                 title='Job Requests', template='gridon', height=300)
                st.plotly_chart(fig_job, use_container_width=True)
        
        with col4:
            # Schedule Demo Requests
            demo_requests = filtered_df[filtered_df['URIStem'].str.startswith('/schedule-demo/')]
            if not demo_requests.empty:
                demo_request_counts = demo_requests['URIStem'].value_counts().reset_index()
                demo_request_counts.columns = ['Demo Type', 'Count']
                
                fig_demo = px.scatter(demo_request_counts, x='Demo Type', y='Count', 
                                      title='Schedule Demo Requests', template='gridon', height=300)
                st.plotly_chart(fig_demo, use_container_width=True)
        
        with col5:
            # Promotional Event Requests
            promo_requests = filtered_df[filtered_df['URIStem'].str.startswith('/promotional-events/')]
            if not promo_requests.empty:
                promo_request_counts = promo_requests['URIStem'].value_counts().reset_index()
                promo_request_counts.columns = ['Promo Type', 'Count']
                
                fig_promo = px.pie(promo_request_counts, names='Promo Type', values='Count',
                                    title='Promotional Event Requests', height=400)
                st.plotly_chart(fig_promo, use_container_width=True)
        
        with col6:
            # Virtual Assistant Requests
            virtual_assist_requests = filtered_df[filtered_df['URIStem'].str.startswith('/virtual-assistant/')]
            if not virtual_assist_requests.empty:
                virtual_assist_request_counts = virtual_assist_requests['URIStem'].value_counts().reset_index()
                virtual_assist_request_counts.columns = ['Request Type', 'Count']
                
                fig_virtual = px.bar(virtual_assist_request_counts, x='Request Type', y='Count',
                                     title='Virtual Assistant Requests', template='gridon', height=300)
                st.plotly_chart(fig_virtual, use_container_width=True)

    elif selected_tab == "Traffic Analysis":
        st.header("Website Traffic Analysis")
        
        # Filter out internal referers
        external_referers = filtered_df[~filtered_df['Referer'].isin(["-", "https://ai-solutions.com"])]
        
        # Process Referer data
        referer_counts = (
            external_referers['Referer']
            .value_counts()
            .reset_index()
        )
        referer_counts.columns = ['Referer', 'Count']
        
        # Calculate percentages only if we have referers
        if not referer_counts.empty:
            total_referers = referer_counts['Count'].sum()
            referer_counts['Percentage'] = (referer_counts['Count'] / total_referers) * 100
            
            # Create a gauge chart for top referer
            top_referer = referer_counts.iloc[0]
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=top_referer['Percentage'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"Top External Referer: {top_referer['Referer']}"},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': 'lightgray'},
                        {'range': [50, 75], 'color': 'gray'},
                        {'range': [75, 100], 'color': 'darkgray'}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': top_referer['Percentage']}
                }
            ))
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Group by referer and calculate total sales
            referer_revenue = (
                external_referers.groupby('Referer')['Sales']
                .sum()
                .reset_index()
                .sort_values('Sales', ascending=False)
            )
            
            # Convert DateTime to date string for plotting
            external_referers['Month'] = external_referers['DateTime'].dt.strftime('%Y-%m')
            
            # Calculate monthly revenue by referer
            monthly_referer_revenue = (
                external_referers.groupby(['Month', 'Referer'])['Sales']
                .sum()
                .unstack()
                .fillna(0)
            )
            
            # Calculate month-over-month growth for top 5 referers
            top_referers = referer_revenue.head(5)['Referer'].tolist()
            monthly_growth = monthly_referer_revenue[top_referers].pct_change() * 100
            
            # Reset index to make Month a column and convert to string
            monthly_growth = monthly_growth.reset_index()
            monthly_growth['Month'] = monthly_growth['Month'].astype(str)
            
            # Plot the growth chart
            fig_growth = px.line(
                monthly_growth,
                x='Month',
                y=top_referers,
                title='Monthly Revenue Growth % by Top Referers',
                labels={'value': 'Growth %', 'Month': 'Month', 'variable': 'Referer'},
                height=350
            )
            fig_growth.update_layout(
                hovermode='x unified',
                yaxis_title='Growth Percentage',
                xaxis_title='Month'
            )
            st.plotly_chart(fig_growth, use_container_width=True)
            
            # Show top 10 referers by revenue in a table
            st.subheader("Top 10 Revenue-Generating Referers")
            st.dataframe(
                referer_revenue.head(10).rename(columns={'Sales': 'Total Revenue'}),
                use_container_width=True
            )
            
            # Bar chart of top referers by count
            st.subheader("Referer Distribution (External Only)")
            fig_bar = px.bar(
                referer_counts.head(10), 
                x='Referer', 
                y='Count',
                color='Referer', 
                height=350,
                labels={'Count': 'Number of Visits', 'Referer': 'Source Website'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("No external referer data available with current filters")

# ===== APP INITIALIZATION =====
def main():
    # Initialize session state for authentication
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    # Show login page or main dashboard based on authentication status
    if not st.session_state["authenticated"]:
        login_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
