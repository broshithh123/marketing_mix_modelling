
import numpy as np
import pandas as pd
from pathlib import Path

# ----------------------------------------
# 1. SET UP THE DATASET
# ----------------------------------------

np.random.seed(42)

weeks = 156

dates = pd.date_range(
    start="2023-01-02",
    periods=weeks,
    freq="W-MON"
)

data = pd.DataFrame({
    "date": dates,
    "week": range(1, weeks + 1)
})

# ----------------------------------------
# 2. GENERATE ADVERTISING SPENDING
# ----------------------------------------

data["tv_spend"] = np.random.uniform(5000, 12000, weeks)

data["search_spend"] = np.random.uniform(2000, 7000, weeks)

data["social_spend"] = np.random.uniform(1500, 6000, weeks)

data["print_spend"] = np.random.uniform(1000, 4000, weeks)

# ----------------------------------------
# 3. GENERATE BUSINESS VARIABLES
# ----------------------------------------

data["price"] = np.random.uniform(45, 65, weeks)

data["promotion"] = np.random.choice(
    [0, 1],
    size=weeks,
    p=[0.75, 0.25]
)

data["holiday"] = np.random.choice(
    [0, 1],
    size=weeks,
    p=[0.85, 0.15]
)

data["competitor_index"] = np.random.uniform(
    0.8, 1.2, weeks
)

# ----------------------------------------
# 4. ADSTOCK FUNCTION
# ----------------------------------------

def apply_adstock(spend, decay=0.5):

    result = np.zeros(len(spend))

    result[0] = spend[0]

    for i in range(1, len(spend)):

        result[i] = (
            spend[i] + decay * result[i - 1]
        )

    return result


# ----------------------------------------
# 5. HILL SATURATION FUNCTION
# ----------------------------------------

def hill_saturation(x, half_saturation, slope=1.5):

    numerator = x ** slope

    denominator = (
        x ** slope + half_saturation ** slope
    )

    return numerator / denominator


# ----------------------------------------
# 6. TRANSFORM ADVERTISING CHANNELS
# ----------------------------------------

data["tv_adstock"] = apply_adstock(
    data["tv_spend"], 0.6
)

data["search_adstock"] = apply_adstock(
    data["search_spend"], 0.3
)

data["social_adstock"] = apply_adstock(
    data["social_spend"], 0.4
)

data["print_adstock"] = apply_adstock(
    data["print_spend"], 0.5
)

data["tv_effect"] = hill_saturation(
    data["tv_adstock"], 25000
)

data["search_effect"] = hill_saturation(
    data["search_adstock"], 8000
)

data["social_effect"] = hill_saturation(
    data["social_adstock"], 9000
)

data["print_effect"] = hill_saturation(
    data["print_adstock"], 7000
)

# ----------------------------------------
# 7. GENERATE WEEKLY REVENUE
# ----------------------------------------

trend = np.linspace(0, 5000, weeks)

seasonality = (
    3000 * np.sin(2 * np.pi * data["week"] / 52)
)

noise = np.random.normal(0, 2500, weeks)

data["sales"] = (
    50000
    + trend
    + seasonality
    + 35000 * data["tv_effect"]
    + 25000 * data["search_effect"]
    + 20000 * data["social_effect"]
    + 12000 * data["print_effect"]
    + 5000 * data["promotion"]
    + 3500 * data["holiday"]
    - 6000 * data["competitor_index"]
    - 500 * data["price"]
    + noise
)

data["sales"] = data["sales"].round(2)

# ----------------------------------------
# 8. SAVE THE DATASET
# ----------------------------------------

project_root = Path(__file__).resolve().parents[1]

output_folder = project_root / "data" / "raw"

output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "marketing_data.csv"

data.to_csv(output_file, index=False)

# ----------------------------------------
# 9. DISPLAY RESULTS
# ----------------------------------------

print("Marketing dataset created successfully!")

print("\nDataset shape:")
print(data.shape)

print("\nFirst five rows:")
print(data.head())

print("\nDataset information:")
print(data.info())

print("\nSales summary:")
print(data["sales"].describe())

print("\nSaved to:")
print(output_file)
