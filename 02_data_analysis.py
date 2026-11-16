
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ----------------------------------------
# 1. LOAD DATASET
# ----------------------------------------

project_root = Path(__file__).resolve().parents[1]

file_path = project_root / "data" / "raw" / "marketing_data.csv"

data = pd.read_csv(file_path, parse_dates=["date"])

print("Dataset loaded successfully!")

# ----------------------------------------
# 2. BASIC DATA UNDERSTANDING
# ----------------------------------------

print("\nDataset shape:")
print(data.shape)

print("\nColumn names:")
print(data.columns.tolist())

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicate rows:")
print(data.duplicated().sum())

print("\nDescriptive statistics:")
print(data.describe().round(2))

# ----------------------------------------
# 3. TOTAL ADVERTISING SPENDING
# ----------------------------------------

channels = [
    "tv_spend",
    "search_spend",
    "social_spend",
    "print_spend"
]

channel_totals = data[channels].sum().sort_values(
    ascending=False
)

print("\nTotal advertising expenditure:")
print(channel_totals.round(2))

# ----------------------------------------
# 4. CREATE OUTPUT FOLDER
# ----------------------------------------

output_folder = project_root / "reports" / "eda"

output_folder.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

# ----------------------------------------
# 5. CHART 1: WEEKLY SALES TREND
# ----------------------------------------

plt.figure(figsize=(12, 5))

plt.plot(
    data["date"],
    data["sales"],
    linewidth=2
)

plt.title("Weekly Sales Trend (2023-2025)")
plt.xlabel("Date")
plt.ylabel("Sales (£)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(output_folder / "sales_trend.png", dpi=300)

plt.show()

# ----------------------------------------
# 6. CHART 2: ADVERTISING SPENDING
# ----------------------------------------

plt.figure(figsize=(9, 5))

channel_totals.plot(kind="bar")

plt.title("Total Advertising Spend by Channel")
plt.xlabel("Marketing Channel")
plt.ylabel("Total Spend (£)")
plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    output_folder / "channel_spending.png",
    dpi=300
)

plt.show()

# ----------------------------------------
# 7. CHART 3: SPENDING TRENDS
# ----------------------------------------

plt.figure(figsize=(12, 6))

for channel in channels:

    plt.plot(
        data["date"],
        data[channel],
        label=channel
    )

plt.title("Weekly Advertising Spending Trends")
plt.xlabel("Date")
plt.ylabel("Advertising Spend (£)")
plt.legend()

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    output_folder / "spending_trends.png",
    dpi=300
)

plt.show()

# ----------------------------------------
# 8. CHART 4: CORRELATION HEATMAP
# ----------------------------------------

correlation_columns = [
    "sales",
    "tv_spend",
    "search_spend",
    "social_spend",
    "print_spend",
    "price",
    "promotion",
    "holiday",
    "competitor_index"
]

correlation = data[correlation_columns].corr()

plt.figure(figsize=(11, 8))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Correlation Between Sales and Business Variables")

plt.tight_layout()

plt.savefig(
    output_folder / "correlation_heatmap.png",
    dpi=300
)

plt.show()

# ----------------------------------------
# 9. SAVE SUMMARY
# ----------------------------------------

summary = data.describe().round(2)

summary.to_csv(
    output_folder / "descriptive_statistics.csv"
)

print("\nEDA completed successfully!")

print("\nCharts and statistics saved in:")
print(output_folder)
