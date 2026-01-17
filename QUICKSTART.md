# 🚀 Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

Open your terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

### Step 2: Generate Sample Data (1 minute)

Create the sample Excel file with realistic market data:

```bash
python generate_sample_data.py
```

Expected output:
```
✅ Sample data generated successfully!
📁 File: sample_mobile_data.xlsx
📊 Records: ~200
🌍 Countries: 9
📱 Brands: ~25
🔧 Operating Systems: 3
```

### Step 3: Run the Dashboard (1 minute)

Start the Streamlit app:

```bash
streamlit run mobile_analytics.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 🎮 First Time Usage

1. **Home Page**: You'll see instructions and a message to upload a file
2. **Upload Sample Data**: Click "Upload Excel file" in the sidebar and select `sample_mobile_data.xlsx`
3. **Select Country**: Use the dropdown to pick a country (e.g., "United States")
4. **Explore Tabs**:
   - 📈 **Trends**: See how brands evolved over 12 months
   - 🏢 **Brand Distribution**: Current market share pie chart
   - 🔧 **OS Distribution**: iOS vs Android comparison
   - 📱 **Usage Patterns**: Daily usage by brand
   - 📊 **Raw Data**: Download data as CSV

## 📊 Sample Data Overview

The generated `sample_mobile_data.xlsx` contains:

**9 Countries:**
- USA, Canada, UK, Germany
- China, India, Japan
- Brazil, Australia

**4 Major Brands** (plus Others):
- Apple (iOS)
- Samsung (Android)
- Xiaomi (Android)
- Oppo, Vivo, Realme, Motorola (Android)

**12 Months** of historical data with:
- Market share percentages
- User counts (in millions)
- Average daily usage (hours)
- Operating system breakdown

## 📁 Files You'll Have

After running the setup:

```
your-directory/
├── mobile_analytics.py          ← Main app (DO NOT MODIFY for basic use)
├── generate_sample_data.py      ← Data generator script
├── sample_mobile_data.xlsx      ← Sample data (created by script)
├── requirements.txt             ← Dependencies list
└── README.md                    ← Full documentation
```

## 🔄 How to Use Your Own Data

1. **Prepare Your Excel File** with these columns:
   - Country
   - Date (format: YYYY-MM-DD)
   - Brand
   - OS
   - Market_Share (numeric)
   - Users_Millions (numeric)
   - Usage_Hours (numeric)

2. **Run the App**:
   ```bash
   streamlit run mobile_analytics.py
   ```

3. **Upload Your File** via the sidebar

4. **Select a Country** and explore!

## ⚙️ Basic Customization

### Change the Title
Edit `mobile_analytics.py`, find this line:
```python
st.markdown('<div class="title-style">📱 Mobile Phone Market Analytics Dashboard</div>', unsafe_allow_html=True)
```

Change to your preferred title.

### Change Default Colors
In the `<style>` section of `mobile_analytics.py`:
```python
.title-style {
    color: #1f77b4;  ← Change this hex code
}
```

## 🆘 Common Issues

| Problem | Solution |
|---------|----------|
| "streamlit: command not found" | Run `pip install streamlit` again |
| "ModuleNotFoundError: No module named 'pandas'" | Run `pip install -r requirements.txt` |
| "File not found" | Make sure you ran `python generate_sample_data.py` first |
| "No data appears" | Check that Excel file columns match required names exactly |
| "Charts are blank" | Verify Date column is in YYYY-MM-DD format |

## 📱 Mobile Access

To access the dashboard from another device on your network:

1. Find your computer's IP address:
   - **Windows**: `ipconfig` (look for IPv4 Address)
   - **Mac/Linux**: `ifconfig` (look for inet)

2. In another device browser, visit:
   ```
   http://your-computer-ip:8501
   ```

Example: `http://192.168.1.100:8501`

## 💾 Deploying Online

To share your dashboard online, use Streamlit Cloud:

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Deploy your app with one click

## 📚 Next Steps

- Explore the full [README.md](README.md) for advanced features
- Create your own data following the Excel format
- Customize charts and colors to match your branding
- Add filters and additional visualizations

## 🎯 What You Can Do Now

✅ View market trends over 12 months
✅ Compare brands in any country
✅ Analyze iOS vs Android usage
✅ Understand user engagement patterns
✅ Export data for further analysis
✅ Create custom reports by country

---

**You're all set!** 🚀

If you have questions, check the README.md file or the dashboard's built-in help documentation.

Happy analyzing! 📊✨
