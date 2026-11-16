
import pandas as pd
from pathlib import Path

from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side
)

from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter

# ========================================
# 1. PROJECT PATHS
# ========================================

project_root = Path(__file__).resolve().parents[1]

data_path = project_root / "data" / "raw" / "marketing_data.csv"

model_path = project_root / "reports" / "model"

output_folder = project_root / "reports"

output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "Marketing_Performance_Report.xlsx"

# ========================================
# 2. LOAD EXISTING RESULTS
# ========================================

data = pd.read_csv(data_path, parse_dates=["date"])

channel_data = pd.read_csv(
    model_path / "channel_contributions.csv"
)

metrics_data = pd.read_csv(
    model_path / "model_metrics.csv"
)

# ========================================
# 3. PREPARE MONTHLY DATA
# ========================================

data["month"] = data["date"].dt.to_period("M")

monthly_data = data.groupby("month").agg(
    sales=("sales", "sum"),
    tv_spend=("tv_spend", "sum"),
    search_spend=("search_spend", "sum"),
    social_spend=("social_spend", "sum"),
    print_spend=("print_spend", "sum")
).reset_index()

monthly_data["month"] = monthly_data["month"].astype(str)

# ========================================
# 4. PREPARE QUARTERLY DATA
# ========================================

data["quarter"] = data["date"].dt.to_period("Q")

quarterly_data = data.groupby("quarter").agg(
    sales=("sales", "sum"),
    tv_spend=("tv_spend", "sum"),
    search_spend=("search_spend", "sum"),
    social_spend=("social_spend", "sum"),
    print_spend=("print_spend", "sum")
).reset_index()

quarterly_data["quarter"] = quarterly_data["quarter"].astype(str)

# ========================================
# 5. CREATE EXECUTIVE SUMMARY
# ========================================

total_sales = data["sales"].sum()

average_weekly_sales = data["sales"].mean()

total_spend = data[
    ["tv_spend", "search_spend", "social_spend", "print_spend"]
].sum().sum()

overall_roas = (
    channel_data["estimated_contribution"].sum()
    / total_spend
)

executive_summary = pd.DataFrame({
    "Business KPI": [
        "Total Revenue",
        "Average Weekly Revenue",
        "Total Advertising Spend",
        "Estimated Marketing ROAS",
        "Number of Weeks Analysed"
    ],
    "Value": [
        total_sales,
        average_weekly_sales,
        total_spend,
        overall_roas,
        len(data)
    ]
})

# ========================================
# 6. CREATE EXCEL WORKBOOK
# ========================================

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    executive_summary.to_excel(
        writer,
        sheet_name="Executive Summary",
        index=False
    )

    channel_data.to_excel(
        writer,
        sheet_name="Channel Performance",
        index=False
    )

    metrics_data.to_excel(
        writer,
        sheet_name="Model Metrics",
        index=False
    )

    monthly_data.to_excel(
        writer,
        sheet_name="Monthly Trends",
        index=False
    )

    quarterly_data.to_excel(
        writer,
        sheet_name="Quarterly Trends",
        index=False
    )

    data.to_excel(
        writer,
        sheet_name="Weekly Data",
        index=False
    )

# ========================================
# 7. FORMAT EXCEL WORKBOOK
# ========================================

from openpyxl import load_workbook

workbook = load_workbook(output_file)

header_fill = PatternFill(
    "solid",
    fgColor="1F4E78"
)

header_font = Font(
    bold=True,
    color="FFFFFF",
    size=11
)

thin_border = Border(
    bottom=Side(style="thin", color="D9E2F3")
)

for sheet in workbook.worksheets:

    sheet.freeze_panes = "A2"

    sheet.auto_filter.ref = sheet.dimensions

    for cell in sheet[1]:

        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    for column_cells in sheet.columns:

        column_letter = get_column_letter(
            column_cells[0].column
        )

        max_length = 0

        for cell in column_cells:

            if cell.value is not None:

                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

            cell.border = thin_border

        sheet.column_dimensions[column_letter].width = min(
            max_length + 4,
            32
        )

    sheet.row_dimensions[1].height = 25

# ========================================
# 8. FORMAT CURRENCY AND ROAS
# ========================================

currency_columns = {
    "Executive Summary": ["B2", "B3", "B4"],
    "Channel Performance": ["B2", "C2", "B3", "C3", "B4", "C4", "B5", "C5"],
    "Monthly Trends": [],
    "Quarterly Trends": []
}

for sheet_name, cells in currency_columns.items():

    sheet = workbook[sheet_name]

    for cell_reference in cells:

        sheet[cell_reference].number_format = '£#,##0.00'

# Executive Summary ROAS

workbook["Executive Summary"]["B5"].number_format = '0.00x'

# Channel Performance formatting

channel_sheet = workbook["Channel Performance"]

for row in range(2, channel_sheet.max_row + 1):

    channel_sheet.cell(row, 2).number_format = '£#,##0.00'

    channel_sheet.cell(row, 3).number_format = '£#,##0.00'

    channel_sheet.cell(row, 4).number_format = '0.00x'

# Model metrics formatting

metrics_sheet = workbook["Model Metrics"]

for row in range(2, metrics_sheet.max_row + 1):

    metrics_sheet.cell(row, 2).number_format = '#,##0.0000'

# Monthly and quarterly currency formatting

for sheet_name in ["Monthly Trends", "Quarterly Trends"]:

    sheet = workbook[sheet_name]

    for row in range(2, sheet.max_row + 1):

        for col in range(2, sheet.max_column + 1):

            sheet.cell(row, col).number_format = '£#,##0.00'

# ========================================
# 9. ADD CHANNEL PERFORMANCE CHART
# ========================================

channel_chart = BarChart()

channel_chart.title = "Estimated ROAS by Channel"

channel_chart.y_axis.title = "ROAS"

channel_chart.x_axis.title = "Marketing Channel"

channel_chart.style = 10

channel_chart.height = 8

channel_chart.width = 15

channel_data_ref = Reference(
    channel_sheet,
    min_col=4,
    min_row=1,
    max_row=5
)

channel_categories = Reference(
    channel_sheet,
    min_col=1,
    min_row=2,
    max_row=5
)

channel_chart.add_data(
    channel_data_ref,
    titles_from_data=True
)

channel_chart.set_categories(channel_categories)

channel_sheet.add_chart(
    channel_chart,
    "F2"
)

# ========================================
# 10. ADD MONTHLY SALES CHART
# ========================================

monthly_sheet = workbook["Monthly Trends"]

monthly_chart = LineChart()

monthly_chart.title = "Monthly Revenue Trend"

monthly_chart.y_axis.title = "Revenue (£)"

monthly_chart.x_axis.title = "Month"

monthly_chart.style = 13

monthly_chart.height = 9

monthly_chart.width = 18

monthly_values = Reference(
    monthly_sheet,
    min_col=2,
    min_row=1,
    max_row=monthly_sheet.max_row
)

monthly_categories = Reference(
    monthly_sheet,
    min_col=1,
    min_row=2,
    max_row=monthly_sheet.max_row
)

monthly_chart.add_data(
    monthly_values,
    titles_from_data=True
)

monthly_chart.set_categories(monthly_categories)

monthly_sheet.add_chart(
    monthly_chart,
    "H2"
)

# ========================================
# 11. ADD QUARTERLY SALES CHART
# ========================================

quarterly_sheet = workbook["Quarterly Trends"]

quarterly_chart = LineChart()

quarterly_chart.title = "Quarterly Revenue Trend"

quarterly_chart.y_axis.title = "Revenue (£)"

quarterly_chart.x_axis.title = "Quarter"

quarterly_chart.style = 13

quarterly_chart.height = 9

quarterly_chart.width = 18

quarterly_values = Reference(
    quarterly_sheet,
    min_col=2,
    min_row=1,
    max_row=quarterly_sheet.max_row
)

quarterly_categories = Reference(
    quarterly_sheet,
    min_col=1,
    min_row=2,
    max_row=quarterly_sheet.max_row
)

quarterly_chart.add_data(
    quarterly_values,
    titles_from_data=True
)

quarterly_chart.set_categories(quarterly_categories)

quarterly_sheet.add_chart(
    quarterly_chart,
    "H2"
)

# ========================================
# 12. SAVE FINAL REPORT
# ========================================

workbook.save(output_file)

print("\n================================")
print("EXCEL REPORT CREATED SUCCESSFULLY!")
print("================================")

print("\nReport location:")
print(output_file)

print("\nWorksheets created:")

for sheet in workbook.sheetnames:

    print("-", sheet)
