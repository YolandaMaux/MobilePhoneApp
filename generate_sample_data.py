import pandas as pd
import numpy as np
from datetime import datetime, timedelta

"""
Sample Mobile Phone Market Data Generator

This script creates sample mobile phone market data by country
and returns it as a pandas DataFrame.
"""

def generate_sample_data():
    """Generate sample mobile phone market data and return as DataFrame."""

    # Define countries and their characteristics
    countries = {
        'United States': {
            'primary_brands': ['Apple', 'Samsung', 'Google', 'Motorola'],
            'primary_os': ['iOS', 'Android'],
            'base_users': 280,
            'growth_rate': 0.02,
            'ios_preference': 0.58,
            'top_brands': {
                'Apple': 0.51,
                'Samsung': 0.24,
                'Google': 0.13,
                'Motorola': 0.08,
                'Others': 0.04
            }
        },
        'Canada': {
            'primary_brands': ['Apple', 'Samsung', 'Google'],
            'primary_os': ['iOS', 'Android'],
            'base_users': 35,
            'growth_rate': 0.015,
            'ios_preference': 0.60,
            'top_brands': {
                'Apple': 0.61,
                'Samsung': 0.23,
                'Google': 0.08,
                'Others': 0.08
            }
        },
        'United Kingdom': {
            'primary_brands': ['Apple', 'Samsung', 'Google'],
            'primary_os': ['iOS', 'Android'],
            'base_users': 55,
            'growth_rate': 0.01,
            'ios_preference': 0.57,
            'top_brands': {
                'Apple': 0.51,
                'Samsung': 0.31,
                'Google': 0.05,
                'Others': 0.13
            }
        },
        'Germany': {
            'primary_brands': ['Samsung', 'Apple', 'Xiaomi'],
            'primary_os': ['Android', 'iOS'],
            'base_users': 65,
            'growth_rate': 0.005,
            'ios_preference': 0.37,
            'top_brands': {
                'Samsung': 0.34,
                'Apple': 0.37,
                'Xiaomi': 0.12,
                'Others': 0.17
            }
        },
        'China': {
            'primary_brands': ['Huawei', 'Oppo', 'Vivo', 'Xiaomi', 'Apple'],
            'primary_os': ['Android', 'iOS'],
            'base_users': 975,
            'growth_rate': 0.03,
            'ios_preference': 0.24,
            'top_brands': {
                'Huawei': 0.20,
                'Oppo': 0.18,
                'Vivo': 0.15,
                'Xiaomi': 0.13,
                'Apple': 0.14,
                'Others': 0.20
            }
        },
        'India': {
            'primary_brands': ['Xiaomi', 'Realme', 'Oppo', 'Samsung', 'Apple'],
            'primary_os': ['Android', 'iOS'],
            'base_users': 659,
            'growth_rate': 0.08,
            'ios_preference': 0.04,
            'top_brands': {
                'Xiaomi': 0.19,
                'Realme': 0.14,
                'Oppo': 0.12,
                'Samsung': 0.18,
                'Apple': 0.04,
                'Vivo': 0.10,
                'Others': 0.23
            }
        },
        'Japan': {
            'primary_brands': ['Apple', 'Samsung', 'Sharp'],
            'primary_os': ['iOS', 'Android'],
            'base_users': 97,
            'growth_rate': 0.01,
            'ios_preference': 0.69,
            'top_brands': {
                'Apple': 0.59,
                'Samsung': 0.07,
                'Sharp': 0.10,
                'Others': 0.24
            }
        },
        'Brazil': {
            'primary_brands': ['Samsung', 'Motorola', 'Xiaomi'],
            'primary_os': ['Android', 'iOS'],
            'base_users': 143,
            'growth_rate': 0.05,
            'ios_preference': 0.16,
            'top_brands': {
                'Samsung': 0.37,
                'Motorola': 0.22,
                'Xiaomi': 0.18,
                'Oppo': 0.10,
                'Others': 0.13
            }
        },
        'Australia': {
            'primary_brands': ['Apple', 'Samsung', 'Google'],
            'primary_os': ['iOS', 'Android'],
            'base_users': 20,
            'growth_rate': 0.02,
            'ios_preference': 0.57,
            'top_brands': {
                'Apple': 0.57,
                'Samsung': 0.26,
                'Google': 0.07,
                'Others': 0.10
            }
        }
    }

    # Generate data
    data_records = []
    start_date = datetime.now() - timedelta(days=365)

    for country, info in countries.items():
        # Generate 12 monthly data points
        for month_offset in range(0, 13):
            current_date = start_date + timedelta(days=30 * month_offset)

            # Calculate users for this month
            month_users = info['base_users'] * (1 + info['growth_rate']) ** month_offset

            # Add some randomness
            noise = np.random.normal(1, 0.02)
            month_users *= noise

            # Generate brand data
            for brand, market_share in info['top_brands'].items():
                # Add slight variation over time
                variation = np.random.normal(1, 0.05)
                adjusted_share = max(
                    0.5,
                    min(8, market_share * variation * 100)
                )  # Market share as percentage

                # Determine OS for this brand
                if brand == 'Apple':
                    os_name = 'iOS'
                elif brand in ['Huawei'] and country == 'China':
                    os_name = 'HarmonyOS'
                else:
                    os_name = 'Android'

                # Calculate users for this brand
                brand_users = month_users * (market_share / 100)

                # Generate usage hours (varies by brand and region)
                if brand == 'Apple':
                    base_usage = 5.5
                elif brand == 'Samsung':
                    base_usage = 4.8
                elif brand == 'Xiaomi':
                    base_usage = 4.5
                else:
                    base_usage = 4.2

                usage_variation = np.random.normal(1, 0.1)
                usage_hours = max(2, base_usage * usage_variation)

                data_records.append({
                    'Country': country,
                    'Date': current_date.strftime('%Y-%m-%d'),
                    'Brand': brand,
                    'OS': os_name,
                    'Market_Share': adjusted_share,
                    'Users_Millions': round(brand_users, 2),
                    'Usage_Hours': round(usage_hours, 2)
                })

    # Create DataFrame in memory and return it
    df = pd.DataFrame(data_records)

    # Optional: print a brief summary/preview, still all in memory
    print("✅ Sample data generated in memory.")
    print(f"📊 Records: {len(df)}")
    print(f"🌍 Countries: {df['Country'].nunique()}")
    print(f"📱 Brands: {df['Brand'].nunique()}")
    print(f"🔧 Operating Systems: {df['OS'].nunique()}")
    print("\nData Preview:")
    print(df.head(10))

    return df


if __name__ == "__main__":
    df = generate_sample_data()
