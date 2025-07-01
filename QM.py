import pandas as pd
import random

# --- Configuration ---
file_path = 'Q32025.csv'
max_shift_special = 4
max_shift_default = 9
special_limit_names = ['Jak Betty', 'Vikrant Bhutani']

# --- Load and Prepare Data ---
data = pd.read_csv(file_path, dayfirst=True)
data.rename(columns={data.columns[0]: "Name"}, inplace=True)

names = data['Name'].tolist()
shift_count = {name: 0 for name in names}
max_shifts = {name: (max_shift_special if name in special_limit_names else max_shift_default) for name in names}

assignments = []
missing_days = []
last_qm = None

# --- Helper: Check if date is Thursday ---
def is_thursday(date):
    return pd.to_datetime(date, dayfirst=True).weekday() == 3

# --- Shift Assignment Loop ---
for date in data.columns[1:]:
    available = data[data[date] == 'Yes']['Name'].tolist()

    # Exclude "Jak Betty" on Thursdays
    if is_thursday(date):
        available = [p for p in available if p != 'Jak Betty']

    # Filter eligible people by shift limit and last assignment
    eligible = [p for p in available if shift_count[p] < max_shifts[p] and p != last_qm]
    if not eligible:
        eligible = [p for p in available if shift_count[p] < max_shifts[p]]

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

# --- Save Assignments to Horizontal CSV ---
sorted_assignments = sorted(assignments, key=lambda x: pd.to_datetime(x["Date"], dayfirst=True))
horizontal_data = {entry["Date"]: entry["Name"] for entry in sorted_assignments}
horizontal_df = pd.DataFrame([horizontal_data])
horizontal_df.to_csv('QM_Assignments.csv', index=False)

# --- Save Unassigned Days ---
if missing_days:
    missing_df = pd.DataFrame(missing_days)
    missing_df.to_csv('Unassigned_Days_Report.csv', index=False)
    print("⚠️ Some days were unassigned. See: Unassigned_Days_Report.csv")

# --- Save Shift Count Summary ---
shift_summary_df = pd.DataFrame(list(shift_count.items()), columns=["Name", "Total Shifts"])
shift_summary_df.to_csv("Shift_Count_Summary.csv", index=False)

# --- Print Shift Summary ---
print("\n📋 Shift Assignment Summary:")
for name, count in shift_count.items():
    print(f"  {name}: {count} shifts")

print("\n✅ Balanced QM assignment saved to: QM_Assignments.csv")
print("📄 Shift count summary saved to: Shift_Count_Summary.csv")
