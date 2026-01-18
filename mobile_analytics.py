import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from pathlib import Path
from generate_sample_data import generate_sample_data  

if "run_button_success" not in st.session_state:
    st.session_state.run_button_success = False


icon = Image.open("mobieAppLogo.png")  # or .ico, .jpg, etc.

# Page configuration
st.set_page_config(
    page_title="Mobile Market Analytics",
    page_icon=icon, #"📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)

# Control metric font sizes
def custom_metric(col, label, value, font_size=20):
    """Display a custom metric with controllable font size"""
    col.markdown(f"""
        <div style='text-align: center;'>
            <p style='font-size: 14px; margin: 0;'>{label}</p>
            <p style='font-size: {font_size}px; font-weight: bold; margin: 0;'>{value}</p>
        </div>
    """, unsafe_allow_html=True)

# Keep your original code as-is



def img_to_base64(img_path: str) -> str:
    img_bytes = Path(img_path).read_bytes()
    return base64.b64encode(img_bytes).decode()

img_base64 = img_to_base64("mobieAppLogo.png")  # your local file

st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:10px;">
        <img src="data:image/png;base64,{img_base64}" width="110">
        <div class="title-style">Mobile Phone Market Analytics</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# -----------------------------
# Sidebar configuration
# -----------------------------
st.sidebar.header("⚙️ Configuration")

st.sidebar.subheader("📚 Sources", help="Check the sources to query.")
source_google_play = st.sidebar.checkbox("Google Play", value=True)
source_app_store = st.sidebar.checkbox("App Store", value=True)
source_other = st.sidebar.checkbox("Other", value=False)

st.sidebar.subheader("⚙️ Settings", help="Add additional info.")
api_key = st.sidebar.text_input("key")
instructions_text = st.sidebar.text_area("Instructions", height=120)

st.sidebar.subheader("⏱️ Time Range", help="Select the time range for query.")
time_range = st.sidebar.selectbox(
    "Select time range",
    ["Last 7 days", "Last 30 days", "Last year", "Last 5 years"], index=2,
)

#st.sidebar.subheader("▶️ Run")
#run_generation = st.sidebar.button("Run",)

# Map timerange to something generate_sample_data could use in future (kept for UI only)
range_map = {
    "Last 7 days": "7d",
    "Last 30 days": "30d",
    "Last year": "1y",
    "Last 5 years": "5y",
}
selected_range_code = range_map.get(time_range, "1y")

# -----------------------------
# Data loading: in-memory only
# -----------------------------
data = None




# Button with color styling based on session state
col1, col2 = st.sidebar.columns([3, 1])
with col1:
    run_generation = st.button("Run", use_container_width=True)

# Apply button color based on success state
if st.session_state.run_button_success:
    st.markdown("""
        <style>
        button[kind="primary"] {
            background-color: #28a745 !important;  /* Green */
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        button[kind="primary"] {
            background-color: #0066cc !important;  /* Blue */
        }
        </style>
    """, unsafe_allow_html=True)

# if run_generation:
#     # Directly generate a fresh DataFrame in memory, no Excel involved. [file:1][file:2]
#     try:
#         data = generate_sample_data()
#         st.sidebar.success("Data generated in memory and loaded into the app.")
#         st.session_state["generated_data"] = data
#     except Exception as e:
#         st.sidebar.error(f"Error generating in-memory data: {e}")

if run_generation:
    try:
        data = generate_sample_data()
        st.session_state["generated_data"] = data
        st.session_state.run_button_success = True  # ✅ Now safe to set
        st.sidebar.success("Data generated in memory and loaded into the app.")
        st.rerun()  # Rerun to apply green color
    except Exception as e:
        st.sidebar.error(f"Error generating in-memory data: {e}")
        st.session_state.run_button_success = False


# If user already generated data earlier this session, reuse it.
if data is None and "generated_data" in st.session_state:
    data = st.session_state["generated_data"]

if data is not None:
    st.sidebar.success("Data loaded successfully!")
    st.sidebar.info(f"Records: {len(data)} | Columns: {len(data.columns)}")
else:
    st.info(
        "How to Use This Dashboard\n\n"
        "1. Configure options in the sidebar and press **Run**.\n"
        "2. Data will be generated in memory (no files needed).\n"
        "3. Select a country and explore the tabs."
    )

# -----------------------------
# Main analytics UI
# -----------------------------
if data is not None:
    if "Country" in data.columns:
        countries = sorted(data["Country"].unique())
        selected_country = st.selectbox(
            "Select Country",
            countries,
            help="Choose a country to view mobile market data",
        )

        country_data = data[data["Country"] == selected_country].copy()

        if not country_data.empty:
            st.subheader(f"Market Analysis - {selected_country}")
            st.markdown("---")

            # Normalize column names from generator to names used below. [file:1]
            rename_map = {
                "Market_Share": "MarketShare",
                "Users_Millions": "UsersMillions",
                "Usage_Hours": "UsageHours",
            }
            country_data = country_data.rename(columns=rename_map)

            # Ensure Date column is datetime
            if "Date" in country_data.columns:
                country_data["Date"] = pd.to_datetime(country_data["Date"], errors="coerce")

            # Top metrics
            col1, col2, col3, col4 = st.columns(4)

            # if "Date" in country_data.columns:
            #     latest_date = country_data["Date"].max()
            #     earliest_date = country_data["Date"].min()
            #     col1.metric("Latest Data Date", str(latest_date.date()) if pd.notnull(latest_date) else "N/A")
            #     col2.metric("Earliest Data Date", str(earliest_date.date()) if pd.notnull(earliest_date) else "N/A")

            # if "MarketShare" in country_data.columns:
            #     avg_share = country_data["MarketShare"].mean()
            #     col3.metric("Average Market Share", f"{avg_share:.2f}")

            # if "UsageHours" in country_data.columns:
            #     avg_usage = country_data["UsageHours"].mean()
            #     col4.metric("Average Daily Usage (hours)", f"{avg_usage:.2f}")

            if "Date" in country_data.columns:
                latest_date = country_data["Date"].max()
                earliest_date = country_data["Date"].min()
                custom_metric(col1, "Start Date", str(earliest_date.date()) if pd.notnull(earliest_date) else "N/A", font_size=20)
                custom_metric(col2, "End Data ", str(latest_date.date()) if pd.notnull(latest_date) else "N/A", font_size=20)
            
            if "MarketShare" in country_data.columns:
                avg_share = country_data["MarketShare"].mean()
                custom_metric(col3, "Average Market Share", f"{avg_share:.2f}", font_size=20)
            
            if "UsageHours" in country_data.columns:
                avg_usage = country_data["UsageHours"].mean()
                custom_metric(col4, "Average Daily Usage (hours)", f"{avg_usage:.2f}", font_size=20)
            
            



            st.markdown("---")

            # Tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["📈 Trends", "🏢 Brand Distribution", "📱 OS Distribution", "📊 Usage Patterns", "📄 Raw Data"]
            )

            # -----------------------------
            # Tab 1: Trends Over Time
            # -----------------------------
            with tab1:
                st.subheader("Market Trends Over Time")

                if "Date" in country_data.columns and "Brand" in country_data.columns:
                    brand_trend = (
                        country_data.groupby(["Date", "Brand"])["MarketShare"]
                        .sum()
                        .reset_index()
                    )

                    if not brand_trend.empty:
                        fig = px.line(
                            brand_trend,
                            x="Date",
                            y="MarketShare",
                            color="Brand",
                            title="Brand Market Share Trend (Past Year)",
                            markers=True,
                            labels={"MarketShare": "Market Share", "Date": "Date"},
                        )
                        fig.update_layout(height=500, hovermode="x unified")
                        st.plotly_chart(fig, use_container_width=True)

                if "Date" in country_data.columns and "OS" in country_data.columns:
                    os_trend = (
                        country_data.groupby(["Date", "OS"])["MarketShare"]
                        .sum()
                        .reset_index()
                    )

                    if not os_trend.empty:
                        fig = px.line(
                            os_trend,
                            x="Date",
                            y="MarketShare",
                            color="OS",
                            title="Operating System Market Share Trend (Past Year)",
                            markers=True,
                            labels={"MarketShare": "Market Share", "Date": "Date"},
                        )
                        fig.update_layout(height=500, hovermode="x unified")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(
                        "No time series data available. Please ensure the data has Date and Brand columns."
                    )

            # -----------------------------
            # Tab 2: Brand Distribution
            # -----------------------------
            with tab2:
                st.subheader("Phone Brand Distribution")

                if "Brand" in country_data.columns and "MarketShare" in country_data.columns:
                    if "Date" in country_data.columns:
                        latest_data = country_data[country_data["Date"] == country_data["Date"].max()]
                    else:
                        latest_data = country_data

                    brand_data = (
                        latest_data.groupby("Brand")["MarketShare"]
                        .sum()
                        .reset_index()
                        .sort_values("MarketShare", ascending=False)
                    )

                    if not brand_data.empty:
                        col1, col2 = st.columns(2)

                        with col1:
                            fig = px.pie(
                                brand_data,
                                values="MarketShare",
                                names="Brand",
                                title="Current Brand Market Share Distribution",
                                hole=0.3,
                            )
                            fig.update_layout(height=500)
                            st.plotly_chart(fig, use_container_width=True)

                        with col2:
                            st.dataframe(
                                brand_data.rename(columns={"MarketShare": "Share"}),
                                use_container_width=True,
                                hide_index=True,
                            )
                    else:
                        st.info("No brand data available.")
                else:
                    st.info("Please ensure the data has Brand and MarketShare columns.")

            # -----------------------------
            # Tab 3: OS Distribution
            # -----------------------------
            with tab3:
                st.subheader("Operating System Distribution")

                if "OS" in country_data.columns and "MarketShare" in country_data.columns:
                    if "Date" in country_data.columns:
                        latest_data = country_data[country_data["Date"] == country_data["Date"].max()]
                    else:
                        latest_data = country_data

                    os_data = (
                        latest_data.groupby("OS")["MarketShare"]
                        .sum()
                        .reset_index()
                        .sort_values("MarketShare", ascending=False)
                    )

                    if not os_data.empty:
                        col1, col2 = st.columns(2)

                        with col1:
                            fig = px.bar(
                                os_data,
                                x="OS",
                                y="MarketShare",
                                title="Current OS Market Share",
                                labels={"MarketShare": "Market Share", "OS": "Operating System"},
                                color="OS",
                            )
                            fig.update_layout(height=500, showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)

                        with col2:
                            st.dataframe(
                                os_data.rename(columns={"MarketShare": "Share"}),
                                use_container_width=True,
                                hide_index=True,
                            )
                    else:
                        st.info("No OS data available.")
                else:
                    st.info("Please ensure the data has OS and MarketShare columns.")

            # -----------------------------
            # Tab 4: Usage Patterns
            # -----------------------------
            with tab4:
                st.subheader("User Engagement & Usage Patterns")

                if "UsageHours" in country_data.columns or "UsersMillions" in country_data.columns:
                    col1, col2 = st.columns(2)

                    # Average usage hours by brand
                    with col1:
                        if "UsageHours" in country_data.columns:
                            if "Date" in country_data.columns:
                                latest_data = country_data[country_data["Date"] == country_data["Date"].max()]
                            else:
                                latest_data = country_data

                            brand_usage = (
                                latest_data.groupby("Brand")["UsageHours"]
                                .mean()
                                .reset_index()
                                .sort_values("UsageHours", ascending=True)
                            )

                            fig = px.bar(
                                brand_usage,
                                x="UsageHours",
                                y="Brand",
                                title="Average Daily Usage by Brand (hours)",
                                labels={"UsageHours": "Hours per Day", "Brand": "Brand"},
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)

                    # User base by brand
                    with col2:
                        if "UsersMillions" in country_data.columns:
                            if "Date" in country_data.columns:
                                latest_data = country_data[country_data["Date"] == country_data["Date"].max()]
                            else:
                                latest_data = country_data

                            brand_users = (
                                latest_data.groupby("Brand")["UsersMillions"]
                                .sum()
                                .reset_index()
                                .sort_values("UsersMillions", ascending=False)
                                .head(10)
                            )

                            fig = px.bar(
                                brand_users,
                                x="Brand",
                                y="UsersMillions",
                                title="User Base by Brand (Millions)",
                                labels={"UsersMillions": "Users (Millions)", "Brand": "Brand"},
                                color="Brand",
                            )
                            fig.update_layout(height=400, showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(
                        "Please ensure the data has UsageHours or UsersMillions columns for this analysis."
                    )

            # -----------------------------
            # Tab 5: Raw Data
            # -----------------------------
            with tab5:
                st.subheader("Raw Data View")

                col1, col2 = st.columns(2)
                with col1:
                    show_all = st.checkbox("Show all records", value=False)
                with col2:
                    sort_by = st.selectbox(
                        "Sort by",
                        options=country_data.columns.tolist(),
                        index=0
                        if "Date" not in country_data.columns
                        else list(country_data.columns).index("Date"),
                    )

                if show_all:
                    display_df = country_data.sort_values(sort_by, ascending=False)
                else:
                    display_df = country_data.sort_values(sort_by, ascending=False).head(20)

                st.dataframe(display_df, use_container_width=True, height=600)

                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="Download filtered data as CSV",
                    data=csv,
                    file_name=f"{selected_country}_mobile_data.csv",
                    mime="text/csv",
                )
        else:
            st.warning(f"No data found for {selected_country}.")
    else:
        st.warning("Country column not found in the data. Please ensure your data has a Country column.")
else:
    st.markdown("---")
    # st.markdown(
    #     """
    #     Your data is generated entirely in memory from a built-in sample generator.
    #     The expected columns are:

    #     - Country: Country name (string)
    #     - Date: Date in YYYY-MM-DD format (string)
    #     - Brand: Phone brand name (e.g., Apple, Samsung, Xiaomi)
    #     - OS: Operating system (e.g., iOS, Android, HarmonyOS)
    #     - Market_Share: Market share percentage (numeric)
    #     - Users_Millions: Number of users in millions (numeric)
    #     - Usage_Hours: Average daily usage in hours (numeric)
    #     """
    # )
