
import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ========================================
# 1. LOAD DATASET
# ========================================

project_root = Path(__file__).resolve().parents[1]

file_path = project_root / "data" / "raw" / "marketing_data.csv"

data = pd.read_csv(file_path, parse_dates=["date"])

print("Marketing data loaded successfully!")

# ========================================
# 2. CREATE TREND AND SEASONAL FEATURES
# ========================================

data["trend"] = np.arange(len(data))

data["season_sin"] = np.sin(
    2 * np.pi * data["week"] / 52
)

data["season_cos"] = np.cos(
    2 * np.pi * data["week"] / 52
)

# ========================================
# 3. SELECT MODEL FEATURES
# ========================================

features = [
    "tv_effect",
    "search_effect",
    "social_effect",
    "print_effect",
    "price",
    "promotion",
    "holiday",
    "competitor_index",
    "trend",
    "season_sin",
    "season_cos"
]

X = data[features]
y = data["sales"]

# ========================================
# 4. TRAIN-TEST SPLIT
# ========================================

split_index = int(len(data) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining observations:", len(X_train))
print("Testing observations:", len(X_test))

# ========================================
# 5. STANDARDISE FEATURES
# ========================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ========================================
# 6. RIDGE REGRESSION
# TIME SERIES CROSS-VALIDATION
# ========================================

tscv = TimeSeriesSplit(n_splits=5)

alphas = np.logspace(-3, 3, 50)

best_alpha = None
best_score = float("inf")

for alpha in alphas:

    fold_errors = []

    for train_idx, val_idx in tscv.split(X_train):

        X_fold_train = X_train.iloc[train_idx]
        X_fold_val = X_train.iloc[val_idx]

        y_fold_train = y_train.iloc[train_idx]
        y_fold_val = y_train.iloc[val_idx]

        fold_scaler = StandardScaler()

        X_fold_train_scaled = fold_scaler.fit_transform(
            X_fold_train
        )

        X_fold_val_scaled = fold_scaler.transform(
            X_fold_val
        )

        model = Ridge(alpha=alpha)

        model.fit(X_fold_train_scaled, y_fold_train)

        predictions = model.predict(X_fold_val_scaled)

        error = mean_absolute_error(
            y_fold_val,
            predictions
        )

        fold_errors.append(error)

    average_error = np.mean(fold_errors)

    if average_error < best_score:

        best_score = average_error
        best_alpha = alpha

print("\nBest Ridge alpha:", best_alpha)
print("Best cross-validation MAE:", round(best_score, 2))

# ========================================
# 7. TRAIN FINAL MODEL
# ========================================

final_model = Ridge(alpha=best_alpha)

final_model.fit(X_train_scaled, y_train)

# ========================================
# 8. PREDICT SALES
# ========================================

predictions = final_model.predict(X_test_scaled)

# ========================================
# 9. MODEL EVALUATION
# ========================================

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANCE")
print("--------------------------")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

# ========================================
# 10. EXTRACT COEFFICIENTS
# ========================================

coefficients = final_model.coef_ / scaler.scale_

coefficient_table = pd.DataFrame({
    "feature": features,
    "coefficient": coefficients
})

print("\nMODEL COEFFICIENTS")
print(coefficient_table.round(4))

# ========================================
# 11. CHANNEL CONTRIBUTION AND ROAS
# ========================================

channel_features = {
    "TV": ("tv_effect", "tv_spend"),
    "Search": ("search_effect", "search_spend"),
    "Social Media": ("social_effect", "social_spend"),
    "Print": ("print_effect", "print_spend")
}

contribution_results = []

for channel, (feature, spend_column) in channel_features.items():

    coefficient = coefficient_table.loc[
        coefficient_table["feature"] == feature,
        "coefficient"
    ].iloc[0]

    contribution = (
        data[feature] * coefficient
    ).sum()

    total_spend = data[spend_column].sum()

    roas = contribution / total_spend

    contribution_results.append({
        "channel": channel,
        "estimated_contribution": contribution,
        "total_spend": total_spend,
        "ROAS": roas
    })

channel_summary = pd.DataFrame(contribution_results)

print("\nCHANNEL PERFORMANCE")
print(channel_summary.round(2))

# ========================================
# 12. SAVE MODEL RESULTS
# ========================================

output_folder = project_root / "reports" / "model"

output_folder.mkdir(parents=True, exist_ok=True)

prediction_results = pd.DataFrame({
    "actual_sales": y_test.values,
    "predicted_sales": predictions
})

prediction_results.to_csv(
    output_folder / "sales_predictions.csv",
    index=False
)

channel_summary.to_csv(
    output_folder / "channel_contributions.csv",
    index=False
)

metrics = pd.DataFrame({
    "metric": ["MAE", "RMSE", "R2", "Best Alpha"],
    "value": [mae, rmse, r2, best_alpha]
})

metrics.to_csv(
    output_folder / "model_metrics.csv",
    index=False
)

print("\nMMM completed successfully!")

print("\nResults saved in:")
print(output_folder)
