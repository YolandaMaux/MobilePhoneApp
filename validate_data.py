import pandas as pd
import sys
from pathlib import Path

"""
Excel Data Validator
Checks if your Excel file matches the required format for the Mobile Analytics Dashboard
"""

REQUIRED_COLUMNS = ['Country', 'Date', 'Brand', 'OS', 'Market_Share', 'Users_Millions', 'Usage_Hours']

def validate_excel_file(file_path):
    """Validate Excel file structure and data types"""
    
    print(f"\n{'='*60}")
    print(f"📋 Validating Excel File: {file_path}")
    print(f"{'='*60}\n")
    
    # Check if file exists
    if not Path(file_path).exists():
        print(f"❌ ERROR: File '{file_path}' not found!")
        return False
    
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)
        print(f"✅ File loaded successfully")
        print(f"   📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to load Excel file: {e}")
        return False
    
    # Check for required columns
    print("📋 Checking Required Columns:")
    print("-" * 60)
    all_columns_present = True
    
    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            print(f"✅ {col:20} - Found")
        else:
            print(f"❌ {col:20} - MISSING!")
            all_columns_present = False
    
    if not all_columns_present:
        print(f"\n❌ Missing required columns!")
        print(f"   Required: {', '.join(REQUIRED_COLUMNS)}")
        print(f"   Found: {', '.join(df.columns.tolist())}")
        return False
    
    print()
    
    # Check data types
    print("🔍 Checking Data Types:")
    print("-" * 60)
    
    errors = []
    
    # Country - should be string
    if not all(isinstance(x, str) for x in df['Country'] if pd.notna(x)):
        errors.append("❌ Country: Must contain only text values")
    else:
        print(f"✅ Country:         String")
    
    # Date - should be datetime
    try:
        pd.to_datetime(df['Date'])
        print(f"✅ Date:            DateTime (YYYY-MM-DD)")
    except:
        errors.append("❌ Date: Must be in YYYY-MM-DD format")
        print(f"❌ Date:            Invalid format (expected YYYY-MM-DD)")
    
    # Brand - should be string
    if not all(isinstance(x, str) for x in df['Brand'] if pd.notna(x)):
        errors.append("❌ Brand: Must contain only text values")
    else:
        print(f"✅ Brand:           String")
    
    # OS - should be string
    if not all(isinstance(x, str) for x in df['OS'] if pd.notna(x)):
        errors.append("❌ OS: Must contain only text values")
    else:
        print(f"✅ OS:              String")
    
    # Market_Share - should be numeric
    try:
        pd.to_numeric(df['Market_Share'])
        print(f"✅ Market_Share:    Numeric (percentage)")
    except:
        errors.append("❌ Market_Share: Must contain only numeric values")
        print(f"❌ Market_Share:    Invalid (must be numeric)")
    
    # Users_Millions - should be numeric
    try:
        pd.to_numeric(df['Users_Millions'])
        print(f"✅ Users_Millions:  Numeric")
    except:
        errors.append("❌ Users_Millions: Must contain only numeric values")
        print(f"❌ Users_Millions:  Invalid (must be numeric)")
    
    # Usage_Hours - should be numeric
    try:
        pd.to_numeric(df['Usage_Hours'])
        print(f"✅ Usage_Hours:     Numeric")
    except:
        errors.append("❌ Usage_Hours: Must contain only numeric values")
        print(f"❌ Usage_Hours:     Invalid (must be numeric)")
    
    print()
    
    # Check for missing values
    print("🔎 Checking for Missing Values:")
    print("-" * 60)
    
    missing_data = df.isnull().sum()
    has_missing = False
    
    for col in REQUIRED_COLUMNS:
        missing_count = missing_data[col]
        if missing_count > 0:
            print(f"⚠️  {col:20} - {missing_count} missing values ({missing_count/len(df)*100:.1f}%)")
            has_missing = True
        else:
            print(f"✅ {col:20} - No missing values")
    
    print()
    
    # Data summary
    print("📊 Data Summary:")
    print("-" * 60)
    print(f"✅ Unique Countries: {df['Country'].nunique()}")
    print(f"✅ Unique Brands:    {df['Brand'].nunique()}")
    print(f"✅ Unique OS:        {df['OS'].nunique()}")
    print(f"✅ Date Range:       {df['Date'].min()} to {df['Date'].max()}")
    print(f"✅ Records:          {len(df)}")
    
    # Sample data
    print()
    print("📋 Sample Data (First 5 Rows):")
    print("-" * 60)
    print(df.head().to_string(index=False))
    
    print()
    
    # Final validation result
    if errors:
        print(f"{'='*60}")
        print("❌ VALIDATION FAILED")
        print(f"{'='*60}")
        for error in errors:
            print(error)
        return False
    else:
        print(f"{'='*60}")
        print("✅ VALIDATION SUCCESSFUL!")
        print(f"{'='*60}")
        print(f"Your file is ready to use with the Mobile Analytics Dashboard")
        print(f"Run: streamlit run mobile_analytics.py")
        return True

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        # No file specified, try common names
        possible_files = ['sample_mobile_data.xlsx', 'mobile_data.xlsx', 'data.xlsx']
        file_to_check = None
        
        for file_name in possible_files:
            if Path(file_name).exists():
                file_to_check = file_name
                break
        
        if not file_to_check:
            print("\n📝 Usage: python validate_data.py <excel_file>")
            print("\nExample: python validate_data.py sample_mobile_data.xlsx")
            print("\nOr place your file in the same directory with one of these names:")
            print(f"   - sample_mobile_data.xlsx")
            print(f"   - mobile_data.xlsx")
            print(f"   - data.xlsx")
            sys.exit(1)
    else:
        file_to_check = sys.argv[1]
    
    success = validate_excel_file(file_to_check)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
