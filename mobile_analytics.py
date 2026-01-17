import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="Mobile Market Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .title-style {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title-style">📱 Mobile Phone Market Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for file upload and country selection
st.sidebar.header("⚙️ Configuration")

# File upload
uploaded_file = st.sidebar.file_uploader(
    "Upload Excel file with mobile data",
    type=['xlsx', 'xls'],
    help="Upload an Excel file containing mobile phone market data by country"
)

# Load data
@st.cache_data
def load_data(file):
    """Load data from Excel file"""
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

if uploaded_file is not None:
    data = load_data(uploaded_file)
    
    if data is not None:
        # Display data info
        st.sidebar.success("✅ Data loaded successfully!")
        st.sidebar.info(f"Records: {len(data)} | Columns: {len(data.columns)}")
        
        # Get unique countries
        if 'Country' in data.columns:
            countries = sorted(data['Country'].unique())
            selected_country = st.sidebar.selectbox(
                "Select Country",
                countries,
                help="Choose a country to view mobile market data"
            )
            
            # Filter data for selected country
            country_data = data[data['Country'] == selected_country].copy()
            
            if not country_data.empty:
                st.subheader(f"📊 Market Analysis - {selected_country}")
                st.markdown("---")
                
                # Create columns for metrics
                col1, col2, col3, col4 = st.columns(4)
                
                # Calculate metrics
                if 'Date' in country_data.columns:
                    latest_date = country_data['Date'].max()
                    earliest_date = country_data['Date'].min()
                    col1.metric("Latest Data Date", latest_date)
                    col2.metric("Earliest Data Date", earliest_date)
                
                if 'Market_Share' in country_data.columns:
                    avg_share = country_data['Market_Share'].mean()
                    col3.metric("Average Market Share", f"{avg_share:.2f}%")
                
                if 'Usage_Hours' in country_data.columns:
                    avg_usage = country_data['Usage_Hours'].mean()
                    col4.metric("Average Daily Usage (hours)", f"{avg_usage:.2f}")
                
                st.markdown("---")
                
                # Tabs for different views
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📈 Trends",
                    "🏢 Brand Distribution",
                    "🔧 OS Distribution",
                    "📱 Usage Patterns",
                    "📊 Raw Data"
                ])
                
                # Tab 1: Trends Over Time
                with tab1:
                    st.subheader("Market Trends Over Time")
                    
                    # Check if we have time series data
                    if 'Date' in country_data.columns and 'Brand' in country_data.columns:
                        # Brand trend
                        brand_trend = country_data.groupby(['Date', 'Brand'])['Market_Share'].sum().reset_index()
                        
                        if not brand_trend.empty:
                            fig = px.line(
                                brand_trend,
                                x='Date',
                                y='Market_Share',
                                color='Brand',
                                title='Brand Market Share Trend (Past Year)',
                                markers=True,
                                labels={'Market_Share': 'Market Share (%)', 'Date': 'Date'}
                            )
                            fig.update_layout(height=500, hovermode='x unified')
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # OS trend
                        if 'OS' in country_data.columns:
                            os_trend = country_data.groupby(['Date', 'OS'])['Market_Share'].sum().reset_index()
                            
                            if not os_trend.empty:
                                fig = px.line(
                                    os_trend,
                                    x='Date',
                                    y='Market_Share',
                                    color='OS',
                                    title='Operating System Market Share Trend (Past Year)',
                                    markers=True,
                                    labels={'Market_Share': 'Market Share (%)', 'Date': 'Date'}
                                )
                                fig.update_layout(height=500, hovermode='x unified')
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No time series data available. Please ensure your file has 'Date' and 'Brand' columns.")
                
                # Tab 2: Brand Distribution
                with tab2:
                    st.subheader("Phone Brand Distribution")
                    
                    if 'Brand' in country_data.columns and 'Market_Share' in country_data.columns:
                        # Latest brand data
                        if 'Date' in country_data.columns:
                            latest_data = country_data[country_data['Date'] == country_data['Date'].max()]
                        else:
                            latest_data = country_data
                        
                        brand_data = latest_data.groupby('Brand')['Market_Share'].sum().reset_index().sort_values('Market_Share', ascending=False)
                        
                        if not brand_data.empty:
                            # Pie chart
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                fig = px.pie(
                                    brand_data,
                                    values='Market_Share',
                                    names='Brand',
                                    title='Current Brand Market Share Distribution',
                                    hole=0.3
                                )
                                fig.update_layout(height=500)
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                st.dataframe(
                                    brand_data.rename(columns={'Market_Share': 'Share (%)'}),
                                    use_container_width=True,
                                    hide_index=True
                                )
                        else:
                            st.info("No brand data available.")
                    else:
                        st.info("Please ensure your file has 'Brand' and 'Market_Share' columns.")
                
                # Tab 3: OS Distribution
                with tab3:
                    st.subheader("Operating System Distribution")
                    
                    if 'OS' in country_data.columns and 'Market_Share' in country_data.columns:
                        # Latest OS data
                        if 'Date' in country_data.columns:
                            latest_data = country_data[country_data['Date'] == country_data['Date'].max()]
                        else:
                            latest_data = country_data
                        
                        os_data = latest_data.groupby('OS')['Market_Share'].sum().reset_index().sort_values('Market_Share', ascending=False)
                        
                        if not os_data.empty:
                            # Bar chart
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                fig = px.bar(
                                    os_data,
                                    x='OS',
                                    y='Market_Share',
                                    title='Current OS Market Share',
                                    labels={'Market_Share': 'Market Share (%)', 'OS': 'Operating System'},
                                    color='OS'
                                )
                                fig.update_layout(height=500, showlegend=False)
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                st.dataframe(
                                    os_data.rename(columns={'Market_Share': 'Share (%)'}),
                                    use_container_width=True,
                                    hide_index=True
                                )
                        else:
                            st.info("No OS data available.")
                    else:
                        st.info("Please ensure your file has 'OS' and 'Market_Share' columns.")
                
                # Tab 4: Usage Patterns
                with tab4:
                    st.subheader("User Engagement & Usage Patterns")
                    
                    if 'Usage_Hours' in country_data.columns or 'Users_Millions' in country_data.columns:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if 'Usage_Hours' in country_data.columns:
                                # Brand usage comparison
                                if 'Brand' in country_data.columns:
                                    latest_data = country_data[country_data['Date'] == country_data['Date'].max()] if 'Date' in country_data.columns else country_data
                                    brand_usage = latest_data.groupby('Brand')['Usage_Hours'].mean().reset_index().sort_values('Usage_Hours', ascending=True)
                                    
                                    fig = px.bar(
                                        brand_usage,
                                        x='Usage_Hours',
                                        y='Brand',
                                        title='Average Daily Usage by Brand (hours)',
                                        labels={'Usage_Hours': 'Hours per Day', 'Brand': ''}
                                    )
                                    fig.update_layout(height=400)
                                    st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            if 'Users_Millions' in country_data.columns:
                                # User base by brand
                                if 'Brand' in country_data.columns:
                                    latest_data = country_data[country_data['Date'] == country_data['Date'].max()] if 'Date' in country_data.columns else country_data
                                    brand_users = latest_data.groupby('Brand')['Users_Millions'].sum().reset_index().sort_values('Users_Millions', ascending=False).head(10)
                                    
                                    fig = px.bar(
                                        brand_users,
                                        x='Brand',
                                        y='Users_Millions',
                                        title='User Base by Brand (Millions)',
                                        labels={'Users_Millions': 'Users (Millions)', 'Brand': ''},
                                        color='Brand'
                                    )
                                    fig.update_layout(height=400, showlegend=False)
                                    st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Please ensure your file has 'Usage_Hours' or 'Users_Millions' columns for this analysis.")
                
                # Tab 5: Raw Data
                with tab5:
                    st.subheader("Raw Data View")
                    
                    # Display options
                    col1, col2 = st.columns(2)
                    with col1:
                        show_all = st.checkbox("Show all records", value=False)
                    with col2:
                        sort_by = st.selectbox(
                            "Sort by:",
                            options=country_data.columns.tolist(),
                            index=0 if 'Date' not in country_data.columns else list(country_data.columns).index('Date')
                        )
                    
                    # Display dataframe
                    if show_all:
                        display_df = country_data.sort_values(sort_by, ascending=False)
                    else:
                        display_df = country_data.sort_values(sort_by, ascending=False).head(20)
                    
                    st.dataframe(display_df, use_container_width=True, height=600)
                    
                    # Download button
                    csv = display_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download filtered data as CSV",
                        data=csv,
                        file_name=f"{selected_country}_mobile_data.csv",
                        mime="text/csv"
                    )
            else:
                st.warning(f"No data found for {selected_country}")
        else:
            st.warning("'Country' column not found in the Excel file. Please ensure your file has a 'Country' column.")
else:
    st.info("""
    ### 📋 How to Use This Dashboard
    
    1. **Upload an Excel file** in the sidebar with mobile phone market data
    2. **Select a country** from the dropdown to analyze
    3. **Explore the tabs** to view:
       - 📈 Market trends over the past year
       - 🏢 Brand distribution by market share
       - 🔧 Operating system popularity
       - 📱 User engagement and usage patterns
       - 📊 Raw data and export options
    
    ### 📁 Required Excel File Format
    
    Your Excel file should have the following columns:
    - **Country**: Country name (string)
    - **Date**: Date in YYYY-MM-DD format (datetime)
    - **Brand**: Phone brand name (e.g., Apple, Samsung, Xiaomi)
    - **OS**: Operating system (e.g., iOS, Android, HarmonyOS)
    - **Market_Share**: Market share percentage (numeric)
    - **Users_Millions**: Number of users in millions (numeric)
    - **Usage_Hours**: Average daily usage in hours (numeric)
    
    ### 📊 Sample Data Download
    
    Use the "sample_mobile_data.xlsx" file provided to test the dashboard.
    """)
    
    # Download sample file button
    st.markdown("---")
    st.subheader("📥 Download Sample Data File")
    
    sample_file_path = "sample_mobile_data.xlsx"
    if os.path.exists(sample_file_path):
        with open(sample_file_path, "rb") as f:
            st.download_button(
                label="Download sample_mobile_data.xlsx",
                data=f.read(),
                file_name="sample_mobile_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("Sample file not found in the current directory. Please run the data generation script first.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.9em;'>
    📱 Mobile Market Analytics Dashboard | Created with Streamlit 🚀
</div>
""", unsafe_allow_html=True)
