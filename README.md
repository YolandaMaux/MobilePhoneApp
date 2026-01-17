# 📱 Mobile Phone Market Analytics Dashboard

A comprehensive Streamlit-based dashboard for analyzing mobile phone market data by country, including brand distribution, operating system preferences, usage patterns, and year-over-year trends.

## 🎯 Features

- **Country-Based Analysis**: Select any country to view its mobile market data
- **Brand Distribution**: Visualize market share of different phone brands
- **OS Comparison**: Analyze iOS vs Android and other operating systems
- **Trend Analysis**: View market trends over the past 12 months
- **Usage Patterns**: Understand user engagement and daily usage hours
- **Data Export**: Download filtered data as CSV for further analysis
- **Interactive Charts**: Plotly-based interactive visualizations
- **Responsive Design**: Works on desktop and mobile browsers

## 📋 Required Excel File Format

Your Excel file must contain the following columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| **Country** | String | Country name | "United States", "India", "Japan" |
| **Date** | DateTime | Date in YYYY-MM-DD format | 2025-01-15 |
| **Brand** | String | Phone brand name | "Apple", "Samsung", "Xiaomi" |
| **OS** | String | Operating System | "iOS", "Android", "HarmonyOS" |
| **Market_Share** | Numeric | Market share percentage | 25.5 |
| **Users_Millions** | Numeric | Number of users in millions | 150.75 |
| **Usage_Hours** | Numeric | Average daily usage in hours | 4.5 |

### Example Data Structure

```
Country          | Date       | Brand    | OS      | Market_Share | Users_Millions | Usage_Hours
United States    | 2024-01-15 | Apple    | iOS     | 51.0         | 142.8          | 5.5
United States    | 2024-01-15 | Samsung  | Android | 24.0         | 67.2           | 4.8
India            | 2024-01-15 | Xiaomi   | Android | 19.0         | 125.4          | 4.2
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Required Packages

```bash
pip install streamlit pandas openpyxl plotly numpy
```

Or install from requirements.txt (create this file):

```bash
# requirements.txt
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.10.0
plotly>=5.17.0
numpy>=1.24.0
```

Then run:
```bash
pip install -r requirements.txt
```

### Step 2: Generate Sample Data

Run the data generation script to create sample data:

```bash
python generate_sample_data.py
```

This will create a file named `sample_mobile_data.xlsx` with sample data for 9 countries covering 12 months of market data.

### Step 3: Run the Dashboard

```bash
streamlit run mobile_analytics.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## 📊 Dashboard Tabs

### 1. 📈 Trends Tab
View market trends over time:
- **Brand Market Share Trend**: Shows how each brand's market share evolved over the past year
- **OS Market Share Trend**: Displays iOS vs Android popularity trends

### 2. 🏢 Brand Distribution Tab
Analyze current brand market distribution:
- **Pie Chart**: Visual distribution of market share by brand
- **Data Table**: Exact market share percentages for each brand

### 3. 🔧 OS Distribution Tab
Explore operating system preferences:
- **Bar Chart**: Current OS market share comparison
- **Data Table**: Detailed OS market share statistics

### 4. 📱 Usage Patterns Tab
Understand user engagement:
- **Brand Usage Comparison**: Average daily usage hours by brand
- **User Base Analysis**: Number of users (in millions) by brand

### 5. 📊 Raw Data Tab
Access and export detailed data:
- View raw data with sorting options
- Display first 20 records or all records
- Download filtered data as CSV

## 🎨 Features in Detail

### Country Selection
- Use the sidebar dropdown to select any country in your dataset
- Real-time data filtering based on selection

### Interactive Visualizations
- Hover over charts to see detailed information
- Click legend items to toggle series visibility
- Use Plotly toolbar for zoom, pan, and download options

### Data Export
- Download filtered country data as CSV from the Raw Data tab
- Perfect for further analysis in Excel or other tools

### Responsive Metrics
- Display of latest data date, earliest data date
- Average market share and daily usage calculations
- Dynamic metric cards based on available data

## 📁 File Structure

```
project-directory/
├── mobile_analytics.py           # Main Streamlit app
├── generate_sample_data.py       # Sample data generator
├── sample_mobile_data.xlsx       # Generated sample data
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 💡 Usage Tips

1. **Create Custom Data**: Replace `sample_mobile_data.xlsx` with your own data following the required format

2. **Multiple Countries**: The app automatically loads all countries from your Excel file

3. **Time Series Analysis**: Ensure your Date column has monthly or periodic entries for proper trend visualization

4. **Data Quality**: 
   - Keep date format consistent (YYYY-MM-DD)
   - Ensure market share percentages are numeric
   - Use consistent brand and OS naming across records

5. **Performance**: 
   - The app caches data for faster loading
   - Upload file once and explore multiple countries smoothly
   - Works efficiently with datasets up to 100k+ records

## 🔍 Data Insights from Sample Data

The included sample data includes realistic market shares based on 2025 statistics:

**By Country:**
- **USA**: Apple dominates (51%), followed by Samsung (24%)
- **India**: Xiaomi leads (19%), Android dominance (95%)
- **China**: Diverse market with Huawei, Oppo, Vivo competing
- **Japan**: Strong Apple preference (59% iOS)
- **Brazil**: Samsung leads (37%), followed by Motorola
- **Germany**: Balanced market between Apple and Samsung

**By OS:**
- **Global**: Android ~71%, iOS ~29%
- **Developed Markets**: iOS stronger (40-70%)
- **Emerging Markets**: Android dominance (85-95%)

## 🛠️ Customization

### Change Color Scheme
Edit the CSS in `mobile_analytics.py`:
```python
.title-style {
    color: #your_color;
}
```

### Add More Metrics
Extend the metrics section to include additional KPIs from your data columns

### Modify Chart Types
Replace `px.pie()` or `px.bar()` with other Plotly Express charts like:
- `px.sunburst()` for hierarchical data
- `px.scatter()` for correlation analysis
- `px.box()` for distribution analysis

### Add Filters
Extend the sidebar with additional filters:
```python
brand_filter = st.sidebar.multiselect("Select Brands", brands)
date_range = st.sidebar.date_input("Select Date Range", [start_date, end_date])
```

## 🐛 Troubleshooting

### Issue: "Column not found" error
**Solution**: Ensure your Excel file has all required columns with exact names (case-sensitive):
- Country, Date, Brand, OS, Market_Share, Users_Millions, Usage_Hours

### Issue: No data appears after country selection
**Solution**: Check that your Excel file has data rows for the selected country

### Issue: Charts not displaying
**Solution**: Verify that:
- Date column is in YYYY-MM-DD format
- Market_Share and Users_Millions are numeric (not text)
- Data has at least 2 rows per country for trends

### Issue: Streamlit not found
**Solution**: Ensure installation was successful:
```bash
pip install --upgrade streamlit
streamlit --version
```

## 📈 Expected Data Volume

For optimal performance:
- **Small Dataset**: < 5,000 rows (9 countries × 12 months × 50 brands)
- **Medium Dataset**: 5,000 - 50,000 rows
- **Large Dataset**: 50,000+ rows (may require optimization)

The sample data includes:
- **9 Countries**: USA, Canada, UK, Germany, China, India, Japan, Brazil, Australia
- **12 Months**: Full year of historical data with monthly granularity
- **~200 Records**: Approximately 200 data rows covering all countries and brands

## 📚 Dependencies

- **streamlit**: Web app framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library
- **openpyxl**: Excel file handling
- **numpy**: Numerical computing

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify your Excel file format
3. Ensure all dependencies are installed
4. Review sample data structure as reference

## 🚀 Next Steps

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Generate sample data**: `python generate_sample_data.py`
3. **Run the app**: `streamlit run mobile_analytics.py`
4. **Explore the dashboard** with sample data
5. **Upload your own data** following the required format

---

**Happy analyzing!** 📱📊✨
