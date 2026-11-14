# Marketing Mix Modelling (MMM) & Marketing Performance Dashboard

An end-to-end Marketing Mix Modelling project built with **Python, Machine Learning, SQL-style analytical thinking and Excel** to evaluate marketing channel performance, estimate advertising contributions, measure Return on Ad Spend (ROAS), and support data-driven marketing decisions.

The project combines data generation, exploratory data analysis, predictive modelling and automated Excel reporting into a single analytical workflow.

---

## Project Overview

Marketing teams invest across multiple advertising channels, but understanding which channels contribute most to sales is not always straightforward.

This project demonstrates how Marketing Mix Modelling can be used to:

- Analyse the relationship between marketing expenditure and revenue.
- Estimate the contribution of individual advertising channels.
- Compare channel-level Return on Ad Spend (ROAS).
- Predict sales using a Ridge Regression model.
- Evaluate model performance using standard regression metrics.
- Generate an automated Excel performance report and dashboard.

**Note:** This project uses a synthetically generated marketing dataset for demonstration and portfolio purposes. It does not represent actual company or customer data.

---

## Business Objectives

1. Understand how advertising channels relate to sales performance.
2. Estimate the contribution of TV, Search, Social Media and Print advertising.
3. Compare marketing channel efficiency using estimated ROAS.
4. Develop a predictive model to estimate revenue.
5. Present analytical results through an Excel dashboard for business stakeholders.

---

## Technology Stack

| Category | Tools |
|---|---|
| Programming | Python |
| Data Manipulation | Pandas, NumPy |
| Data Visualisation | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Statistical Modelling | Ridge Regression |
| Model Optimisation | GridSearchCV |
| Reporting | Microsoft Excel, OpenPyXL |
| Development Environment | VS Code, Jupyter Notebook |
| Version Control | Git, GitHub |

---

## Project Structure

```text
marketing_mix_modelling/
│
├── data/
│   ├── raw/
│   │   └── marketing_data.csv
│   │
│   └── processed/
│
├── notebooks/
│   ├── 01_data_generation.py
│   ├── 02_data_analysis.py
│   ├── 03_marketing_mix_model.py
│   ├── 04_excel_report.py
│   └── 05_excel_dashboard.py
│
├── src/
│
├── reports/
│   ├── eda/
│   ├── model/
│   │   ├── sales_predictions.csv
│   │   ├── channel_contributions.csv
│   │   └── model_metrics.csv
│   │
│   └── Marketing_Performance_Report.xlsx
│
└── README.md
```

---

## Project Workflow

### 1. Data Generation

Created a synthetic weekly marketing dataset containing 156 observations and 19 columns.

The dataset includes:

- Weekly sales revenue
- TV advertising expenditure
- Search advertising expenditure
- Social media advertising expenditure
- Print advertising expenditure
- Pricing information
- Promotional activity
- Holiday indicators
- Competitor index
- Time and seasonal variables

The dataset provides a controlled environment for demonstrating marketing analytics and predictive modelling techniques.

### 2. Exploratory Data Analysis (EDA)

Performed exploratory analysis to understand the dataset and identify relationships between marketing variables and sales.

Key activities:

- Data inspection and quality checks
- Descriptive statistical analysis
- Revenue and advertising spend analysis
- Correlation analysis
- Marketing channel comparisons
- Trend and seasonal analysis

Visualisations and descriptive statistics are saved in `reports/eda/`.

### 3. Marketing Mix Modelling

Developed a Ridge Regression model to estimate the relationship between marketing activities and sales revenue.

**Modelling techniques:**

- Time-based training and testing split
- Feature engineering
- Seasonal feature representation
- Ridge Regression
- Hyperparameter optimisation using GridSearchCV
- Cross-validation
- Model evaluation

The model uses marketing channel features alongside other business variables, including price, promotions, competitor activity and seasonal indicators.

### 4. Model Evaluation

The model was evaluated on a held-out test dataset.

| Metric | Result |
|---|---:|
| Training observations | 124 |
| Testing observations | 32 |
| Best Ridge Alpha | 2.6827 |
| Cross-validation MAE | 2,370.90 |
| Test MAE | 1,825.22 |
| Test RMSE | 2,607.99 |
| Test R² Score | 0.8684 |

**Interpretation:**

- The model achieved an R² score of 0.8684 on the test dataset.
- The test MAE was approximately £1,825, meaning the average absolute prediction error was around £1,825 in the dataset's revenue units.
- The RMSE was approximately £2,608, indicating the model's prediction error while penalising larger errors.

These results demonstrate predictive performance on the synthetic dataset, not guaranteed performance on real-world marketing data.

### 5. Marketing Channel Performance

Estimated channel contributions and advertising expenditure were used to calculate channel-level ROAS.

| Marketing Channel | Estimated Contribution | Advertising Spend | Estimated ROAS |
|---|---:|---:|---:|
| TV | £2,528,452.02 | £1,297,600.66 | 1.95x |
| Search | £1,530,509.50 | £714,520.88 | 2.14x |
| Social Media | £1,087,708.74 | £580,723.71 | 1.87x |
| Print | £584,435.25 | £395,571.52 | 1.48x |

**Key observations:**

- Search recorded the highest estimated ROAS at 2.14x.
- TV generated the highest estimated contribution.
- Social Media demonstrated an estimated ROAS of 1.87x.
- Print recorded the lowest estimated ROAS at 1.48x.

These figures provide a basis for comparing model-estimated channel performance.

**ROAS calculation:**

\[
ROAS = \frac{\text{Estimated Channel Contribution}}{\text{Advertising Spend}}
\]

Important: These are model-based contribution estimates, not experimentally verified incremental returns. The synthetic dataset and simplified attribution approach do not establish causal marketing impact.

### 6. Automated Excel Reporting

Developed Python scripts using OpenPyXL to automate Excel reporting.

The workbook includes:

- Executive Summary
- Channel Performance
- Model Metrics
- Monthly Trends
- Quarterly Trends
- Weekly Data
- Marketing Performance Dashboard

The dashboard brings key performance indicators, channel comparisons and revenue trends into one Excel worksheet.

---

## Key Business Insights

Based on the model-estimated results:

1. **Search efficiency:** Search has the highest estimated ROAS, making it an interesting channel for further investigation.
2. **TV contribution:** TV delivers the largest estimated absolute contribution among the four channels.
3. **Channel comparison:** ROAS helps compare estimated contribution relative to advertising expenditure.
4. **Revenue prediction:** Ridge Regression provides a predictive baseline for analysing weekly revenue patterns.
5. **Performance reporting:** An automated Excel dashboard makes model outputs easier to communicate to non-technical stakeholders.

These insights are illustrative and should be validated using real campaign data before making budget allocation decisions.

---

## How to Run the Project

### Prerequisites

- Python 3.10 or later
- Visual Studio Code or another Python IDE
- Microsoft Excel (for viewing the generated report)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/marketing_mix_modelling.git
```

### 2. Navigate to the project directory

```bash
cd marketing_mix_modelling
```

### 3. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy openpyxl jupyter
```

### 4. Generate the marketing dataset

```bash
python notebooks/01_data_generation.py
```

### 5. Perform exploratory data analysis

```bash
python notebooks/02_data_analysis.py
```

### 6. Train the Marketing Mix Model

```bash
python notebooks/03_marketing_mix_model.py
```

### 7. Generate the Excel report

```bash
python notebooks/04_excel_report.py
```

### 8. Create the Excel dashboard

```bash
python notebooks/05_excel_dashboard.py
```

The final Excel report will be available at:

```text
reports/Marketing_Performance_Report.xlsx
```

---

## Project Deliverables

| Deliverable | Description |
|---|---|
| Synthetic Marketing Dataset | Weekly marketing and sales observations |
| EDA Reports | Statistical analysis and visualisations |
| Predictive Model | Ridge Regression sales prediction model |
| Model Evaluation | MAE, RMSE, R² and optimal alpha |
| Channel Analysis | Estimated contribution and ROAS |
| Excel Report | Automated multi-sheet performance report |
| Excel Dashboard | Consolidated marketing performance visualisation |

---

## Future Improvements

Potential extensions to make the project more robust:

- Implement adstock transformations to model the carryover effect of advertising.
- Apply saturation curves to capture diminishing returns.
- Compare Ridge Regression with other modelling approaches.
- Introduce Bayesian Marketing Mix Modelling.
- Add budget optimisation and scenario planning.
- Incorporate real-world marketing campaign data.
- Validate incremental channel impact using experiments or other causal methods.
- Develop an interactive Power BI dashboard.

---

## Skills Demonstrated

- Python programming
- Data cleaning and preprocessing
- Exploratory Data Analysis
- Feature engineering
- Regression modelling
- Hyperparameter tuning
- Cross-validation
- Predictive analytics
- Marketing attribution analysis
- ROAS calculation
- Data visualisation
- Automated Excel reporting
- Business insight communication

---

## Author

**Roshit Borra**

MSc Data Science Student | Aspiring Data Analyst

Interested in Data Analytics, Machine Learning, Marketing Analytics and Business Intelligence.

---

*This project was developed as a portfolio project to demonstrate practical applications of Python, predictive modelling and marketing analytics.*
