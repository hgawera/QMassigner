
import pandas as pd
import random
import os

file_path = 'Q32025.csv'
data = pd.read_csv(file_path, dayfirst=True)

# Rename the first column from '2025' to 'Name'
data.columns.values[0] = "Name"

shift_count = {name: 0 for name in data['Name']}
assignments = []
missing_days = []
last_qm = None

def is_thursday(date):
    return pd.to_datetime(date, dayfirst=True).weekday() == 3

for date in data.columns[1:]:
    available = data[data[date] == 'Yes']['Name'].tolist()

    if is_thursday(date):
        available = [p for p in available if p != 'Jak Betty']

    eligible = [p for p in available if shift_count[p] < 7 and p != last_qm]
    if not eligible:
        eligible = [p for p in available if shift_count[p] < 7]

    if eligible:
        min_count = min(shift_count[p] for p in eligible)
        balanced_pool = [p for p in eligible if shift_count[p] == min_count]

        selected = random.choice(balanced_pool)
        assignments.append({"Name": selected, "Date": date})
        shift_count[selected] += 1
        last_qm = selected
    else:
        assignments.append({"Name": "Unassigned", "Date": date})
        missing_days.append({"Date": date, "Reason": "No eligible person available"})
        last_qm = None

# Convert assignments to horizontal format
sorted_assignments = sorted(assignments, key=lambda x: pd.to_datetime(x["Date"], dayfirst=True))
horizontal_data = {entry["Date"]: entry["Name"] for entry in sorted_assignments}
horizontal_df = pd.DataFrame([horizontal_data])
horizontal_df.to_csv('QM_Assignments.csv', index=False)

# Save any missing/unassigned dates
if missing_days:
    missing_df = pd.DataFrame(missing_days)
    missing_df.to_csv('Unassigned_Days_Report.csv', index=False)
    print("⚠️ Some days were unassigned. See: Unassigned_Days_Report.csv")

print("✅ Balanced QM assignment saved to: QM_Assignments.csv")
