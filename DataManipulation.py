import pandas as pd
import datetime

# This file, take the rota in the csv format with the B, D etc and just the names with no gaps and vacany.
# It produces the Y and N file and splits it into Q's

# Step 1: Load the CSV file
file_path = '2025Rota.csv'  # <-- Replace with your actual file path if needed
df = pd.read_csv(file_path)

# Step 2: Rename columns to sequential day numbers (1 to N), keeping first column as-is
original_columns = df.columns.tolist()
df.columns = [original_columns[0]] + list(range(1, len(original_columns)))

# Step 3: Convert sequential day numbers to date strings using the year in the first column
year = int(df.columns[0])  # e.g., 2025
new_columns = [df.columns[0]]  # First column remains the same

for day_num in df.columns[1:]:
    date = datetime.date(year, 1, 1) + datetime.timedelta(days=day_num - 1)
    date_str = date.strftime("%d/%m/%Y")
    new_columns.append(date_str)

df.columns = new_columns

# Step 4: Replace "B" and "D" with "Yes", everything else with "No"
df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: "Yes" if x in ["B", "D"] else "No")

# Step 5: Filter only columns from the specified year
date_columns = df.columns[1:]
date_objects = pd.to_datetime(date_columns, format="%d/%m/%Y", errors='coerce')

# Map columns with valid 2025 dates
filtered_cols = [col for col, date in zip(date_columns, date_objects) if pd.notna(date) and date.year == year]

# Step 6: Group columns into quarters
quarters = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}

for col in filtered_cols:
    date = pd.to_datetime(col, format="%d/%m/%Y")
    if date.month in [1, 2, 3]:
        quarters["Q1"].append(col)
    elif date.month in [4, 5, 6]:
        quarters["Q2"].append(col)
    elif date.month in [7, 8, 9]:
        quarters["Q3"].append(col)
    elif date.month in [10, 11, 12]:
        quarters["Q4"].append(col)

# Step 7: Save each quarter to CSV
for q, cols in quarters.items():
    quarter_df = df[[df.columns[0]] + cols]
    output_file = f"{q}{year}.csv"
    quarter_df.to_csv(output_file, index=False)
    print(f"Saved {output_file}")
