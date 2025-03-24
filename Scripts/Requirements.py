import os
import re
import difflib
import pandas as pd
import numpy as np
from datetime import datetime

# Define file paths
paid_orders_df = 'Scripts/Filtered & Cleaned Data/PaidOrders.csv'
country_df = 'Scripts/Assessment Material/Country.csv'

# Function to check if files exist
def check_files_exist(file_paths):
    missing_files = [file for file in file_paths if not os.path.exists(file)]
    if missing_files:
        print("Error: The following files do not exist:")
        for file in missing_files:
            print(f" - {file}")
        raise FileNotFoundError("Missing files")
    return True

# Load data
try:
    check_files_exist([paid_orders_df, country_df])
    
    orders_df = pd.read_csv(paid_orders_df, encoding='utf-8', 
                            usecols=["PayoutCountryKey", "PayinCountryKey", "OrderPaid", "SenderKey"],
                            parse_dates=['OrderPaid'])
    country_df = pd.read_csv(country_df, encoding='utf-8', 
                             usecols=["CountryKey", "Country"])
    print("Files read successfully.\n")
except (pd.errors.EmptyDataError, pd.errors.ParserError, FileNotFoundError) as e:
    print(f"Error loading files: {e}")
    exit()

valid_countries = country_df['Country'].str.lower().tolist()

# Function to find the closest match for a country name
def get_closest_match(input_country):
    matches = difflib.get_close_matches(input_country.lower(), valid_countries, n=1, cutoff=0.5)
    return matches[0] if matches else None

# Function to validate country input
def get_valid_country_input(prompt):
    while True:
        country_name = input(prompt).strip()
        if country_name == "":  # Allow empty input
            return None
        if not re.match(r"^[a-zA-Z\s]+$", country_name):
            print("Invalid input. Please enter a valid country name (letters and spaces only).")
            continue
        closest_match = get_closest_match(country_name)
        if closest_match:
            if closest_match.lower() != country_name.lower():
                confirmation = input(f"Did you mean '{closest_match.title()}'? (yes/no): ").strip().lower()
                if confirmation in ["yes", "y"]:
                    return closest_match.title()
                else:
                    print("Please try again.")
            else:
                return closest_match.title()
        else:
            print("No close match found. Please enter a valid country name.")

# Function to get country key from country name
def get_country_key(country_name):
    match = country_df[country_df['Country'].str.lower() == country_name.lower()]
    return match['CountryKey'].values[0] if not match.empty else None

# Function to filter data by country
def filter_data_by_country(df, country_name, key_column):
    if not country_name:
        return df
    country_key = get_country_key(country_name)
    if country_key is None:
        print(f"Error: Country '{country_name}' not found.")
        return df
    return df[df[key_column] == country_key]

# Function to filter DataFrame by date range
def filter_data_by_date(df, start_date, end_date):
    start_date = pd.to_datetime(start_date) if start_date else df['OrderPaid'].min()
    end_date = pd.to_datetime(end_date) if end_date else df['OrderPaid'].max()
    return df[(df['OrderPaid'] >= start_date) & (df['OrderPaid'] <= end_date)]

# Function to display orders per month
def display_orders_per_month(filtered_df):
    # Create a date range covering all months in the data
    min_date = filtered_df['OrderPaid'].min().to_period('M')
    max_date = filtered_df['OrderPaid'].max().to_period('M')
    all_months = pd.period_range(start=min_date, end=max_date, freq='M')
    
    # Group by month and count orders
    orders_per_month = filtered_df.groupby(filtered_df['OrderPaid'].dt.to_period('M'))['OrderPaid'].count().reindex(all_months, fill_value=0).reset_index(name='Orders')
    orders_per_month.rename(columns={'index': 'YearMonth'}, inplace=True)
    
    # Calculate MoM change (%)
    orders_per_month['MoM (%)'] = (orders_per_month['Orders'].pct_change().mul(100).replace([np.inf, -np.inf], 0).fillna(0)).round(2)
    
    # Calculate YoY change (%)
    orders_per_month['Previous_Year_Orders'] = orders_per_month['Orders'].shift(12, fill_value=0)
    orders_per_month['YoY (%)'] = (((orders_per_month['Orders'] - orders_per_month['Previous_Year_Orders']) / orders_per_month['Previous_Year_Orders'].replace(0, np.nan)).mul(100).replace([np.inf, -np.inf], 0).fillna(0)).round(2)
    
    print("\nFiltered Orders per Month:")
    print(orders_per_month.tail(13))
    return orders_per_month.tail(13)

# Function to display 3-month rolling sum of unique customers
def display_3month_rolling_sum(filtered_df):
    customers_per_month = filtered_df.groupby(filtered_df['OrderPaid'].dt.to_period('M'))['SenderKey'].nunique().reset_index(name='TransactingCustomer')
    customers_per_month['3MonthSum'] = customers_per_month['TransactingCustomer'].rolling(window=3, min_periods=1).sum()
    print("\n3-Month Rolling Sum of Unique Customers:")
    print(customers_per_month.tail(13))
    return customers_per_month.tail(13)

# Function to display monthly repeat customers and calculate repeat sender rate
def display_monthly_repeat_customers(filtered_df):
    # Group by sender and month to count orders per sender per month
    customer_orders = filtered_df.groupby(['SenderKey', filtered_df['OrderPaid'].dt.to_period('M')])['OrderPaid'].count().reset_index(name='OrderCount')
    
    # Identify repeat customers (senders with more than one order in a month)
    repeat_customers = customer_orders[customer_orders['OrderCount'] > 1]
    
    # Count the number of repeat customers per month
    repeat_customers_per_month = repeat_customers.groupby('OrderPaid')['SenderKey'].nunique().reset_index(name='RepeatCustomers')
    
    # Calculate the number of active customers per month
    active_customers_per_month = filtered_df.groupby(filtered_df['OrderPaid'].dt.to_period('M'))['SenderKey'].nunique().reset_index(name='ActiveCustomers')
    
    # Merge repeat customers and active customers data
    repeat_customers_per_month = pd.merge(repeat_customers_per_month, active_customers_per_month, on='OrderPaid', how='left')
    
    # Calculate Monthly Repeat Sender Rate (%)
    repeat_customers_per_month['RepeatSenderRate (%)'] = (repeat_customers_per_month['RepeatCustomers'] / repeat_customers_per_month['ActiveCustomers']) * 100
    
    # Replace inf and NaN values with 0
    repeat_customers_per_month['RepeatSenderRate (%)'] = (repeat_customers_per_month['RepeatSenderRate (%)'].replace([np.inf, -np.inf], 0).fillna(0)).round(2)
    
    print("\nMonthly Repeat Customers and Repeat Sender Rate:")
    print(repeat_customers_per_month.tail(13))
    return repeat_customers_per_month.tail(13)

# Get user inputs
start_date = input("Enter the start date (YYYY-MM-DD) or leave blank for all dates: ").strip()
end_date = input("Enter the end date (YYYY-MM-DD) or leave blank for all dates: ").strip()
payin_country = get_valid_country_input("Enter the Payin Country to filter by or leave blank for all regions: ")
payout_country = get_valid_country_input("Enter the Payout Country to filter by or leave blank for all regions: ")

# Apply filters
filtered_df = filter_data_by_date(orders_df, start_date, end_date)
filtered_df = filter_data_by_country(filtered_df, payin_country, 'PayinCountryKey')
filtered_df = filter_data_by_country(filtered_df, payout_country, 'PayoutCountryKey')

# Check if data exists
df_empty = filtered_df.empty
if df_empty:
    print("No data found for the specified filters.")
else:
    # Create a directory to save CSV files
    output_dir = 'output_data'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save metadata describing the filters
    metadata = {
        "Filter Description": [
            "Start Date", 
            "End Date", 
            "Payin Country", 
            "Payout Country"
        ],
        "Value": [
            start_date if start_date else "All Dates",
            end_date if end_date else "All Dates",
            payin_country if payin_country else "All Countries",
            payout_country if payout_country else "All Countries"
        ]
    }
    metadata_df = pd.DataFrame(metadata)
    metadata_df.to_csv(os.path.join(output_dir, 'metadata.csv'), index=False)
    
    # Save filtered data and calculations
    orders_per_month = display_orders_per_month(filtered_df)
    orders_per_month.to_csv(os.path.join(output_dir, 'orders_per_month.csv'), index=False)
    
    customers_per_month = display_3month_rolling_sum(filtered_df)
    customers_per_month.to_csv(os.path.join(output_dir, '3month_rolling_sum.csv'), index=False)
    
    repeat_customers_per_month = display_monthly_repeat_customers(filtered_df)
    repeat_customers_per_month.to_csv(os.path.join(output_dir, 'monthly_repeat_customers.csv'), index=False)
    
    print(f"\nData has been saved to the '{output_dir}' directory.")