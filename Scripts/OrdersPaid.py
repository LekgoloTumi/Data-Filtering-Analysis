import os.path
import pandas as pd

# Define file path 
file_path = 'Scripts\Assessment Material\Orders.csv'

# Check if file exists
if not os.path.exists(file_path):
    print(f"Error: The file {file_path} does not exist.")

try:
    # Read the CSV file
    df = pd.read_csv(file_path, delimiter=',', encoding='utf-8', usecols=["OrderPaid", "OrderID", "PayinCountryKey", "PayoutCountryKey", "SenderKey"])
    print("File read successfully.\n")
except Exception as e:
    print(f"Error reading the file: {e}")

# Display the number of paid orders
if 'df' in locals():  # Check if the DataFrame was created successfully
    if all(col in df.columns for col in ['OrderPaid', 'OrderID', "SenderKey"]):  # Check if the columns exists
        number_paid_orders = df[
            (~df['OrderPaid'].fillna('').str.contains('1970/01/01')) & 
            (~df['OrderPaid'].fillna('').str.contains('1900/01/01'))
        ]
        number_paid_orders_cleaned = number_paid_orders.drop_duplicates(subset=['OrderID'])
        target_file_path = 'Scripts\Filtered & Cleaned Data\PaidOrders.csv'

        print("Number of Orders Paid: \n")
        print(number_paid_orders_cleaned.count())
        number_paid_orders_cleaned.to_csv(target_file_path, index=False)
        print(f"File created successfully to {target_file_path}")
        
    else:
        print("Error: 'OrderPaid' or 'OrderID' column does not exist in the file.")