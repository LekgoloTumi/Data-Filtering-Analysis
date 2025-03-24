### **Understanding What This Script Does (No Programming Knowledge Needed)**  

This script is like a **smart assistant** that helps organize and analyze transaction data from different countries. Imagine you work for a company that processes **customer orders and payments** worldwide. You want to understand:  
✔ How many orders were paid each month?  
✔ How customer activity changes over time?  
✔ How many customers are repeat buyers?  

This script **reads the transaction records, filters the data based on user choices, analyzes patterns, and saves the results in organized files.**  

---

### **Step-by-Step Explanation**  

#### **1. Checking If the Files Exist**
📂 The script first checks if two important data files are available:  
- **Paid Orders File** (list of all completed transactions).  
- **Country Information File** (list of countries with their unique codes).  

If these files are missing, the script stops and alerts the user.  

---

#### **2. Reading the Data**
📊 If the files are found, the script **loads the data** and prepares it for analysis.  
It focuses on key details like:  
- Which country the money was sent from (**Payin Country**).  
- Which country received the money (**Payout Country**).  
- When the transaction happened (**Order Paid Date**).  
- Who sent the money (**Customer ID**).  

---

#### **3. Asking the User for Filters**
📝 The script asks the user:  
- A **start and end date** (e.g., "Show me transactions from January to March 2024").  
- A **pay-in country** (e.g., "Show only transactions sent from the USA").  
- A **payout country** (e.g., "Show only transactions received in South Africa").  

If a country name is typed incorrectly, the script suggests the closest match (e.g., "Did you mean 'United States' instead of 'Unted Sttes'?").  

---

#### **4. Filtering the Data**
🧐 Based on the user’s choices, the script **removes unnecessary transactions** and keeps only the relevant ones.  
For example, if you asked to see **only transactions from Canada to Germany**, the script will exclude all other transactions.  

---

#### **5. Analyzing the Data**
📈 Now that the script has only the data the user wants, it runs several calculations:  

✅ **Orders Per Month:**  
- Counts how many transactions happened each month.  
- Checks how much the numbers **increased or decreased** compared to the previous month.  

✅ **3-Month Rolling Customer Count:**  
- Finds out how many different customers sent money each month.  
- Shows a **3-month trend** to spot increases or drops in customer activity.  

✅ **Repeat Customers Per Month:**  
- Identifies **customers who sent money more than once in the same month**.  
- Calculates the **percentage of repeat customers**.  

---

#### **6. Saving the Results**
💾 Finally, the script **creates an organized folder** (`output_data`) and saves:  
- **The filtered data** (transactions matching the user’s criteria).  
- **A summary report** of transactions per month.  
- **Customer trends and repeat customer analysis.**  

The user can open these files in **Excel** for further review.  

---

### **Why Is This Useful?**
✅ **Saves Time** – Instead of manually searching through thousands of transactions, the script does it instantly.  
✅ **Prevents Mistakes** – Ensures correct country names and accurate calculations.  
✅ **Finds Trends** – Helps businesses understand customer behavior and adjust strategies.  
