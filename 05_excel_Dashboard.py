
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter


# ---------------------------------------------------------
# 1. FILE PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REPORT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "Marketing_Performance_Report.xlsx"
)

if not REPORT_PATH.exists():
    raise FileNotFoundError(
        f"Excel report not found: {REPORT_PATH}\n"
        "Run 04_excel_report.py first."
    )


# ---------------------------------------------------------
# 2. LOAD EXISTING EXCEL REPORT
# ---------------------------------------------------------

print("Loading existing Excel report...")

wb = load_workbook(REPORT_PATH, data_only=False)

required_sheets = [
    "Executive Summary",
    "Channel Performance",
    "Model Metrics",
    "Monthly Trends",
    "Quarterly Trends",
]

for sheet_name in required_sheets:
    if sheet_name not in wb.sheetnames:
        raise ValueError(
            f"Required worksheet missing: {sheet_name}. "
            "Run 04_excel_report.py first."
        )

# Remove old dashboard if script is being rerun
if "Dashboard" in wb.sheetnames:
    del wb["Dashboard"]

ws = wb.create_sheet("Dashboard", 0)


# ---------------------------------------------------------
# 3. READ EXISTING REPORT DATA
# ---------------------------------------------------------

summary_ws = wb["Executive Summary"]
channel_ws = wb["Channel Performance"]
metrics_ws = wb["Model Metrics"]
monthly_ws = wb["Monthly Trends"]
quarterly_ws = wb["Quarterly Trends"]


def find_summary_value(keyword):
    """Find a KPI value in the Executive Summary sheet."""
    for row in summary_ws.iter_rows(
        min_row=2,
        values_only=True
    ):
        if row[0] is not None:
            if keyword.lower() in str(row[0]).lower():
                return row[1]

    return None


total_revenue = find_summary_value("Total Revenue")
average_revenue = find_summary_value("Average Weekly Revenue")
total_spend = find_summary_value("Total Advertising Spend")
overall_roas = find_summary_value("Estimated Marketing ROAS")
weeks_analysed = find_summary_value("Number of Weeks Analysed")


# Read channel performance
channels = []

for row in channel_ws.iter_rows(
    min_row=2,
    values_only=True
):
    if row[0] is not None:
        channels.append({
            "name": row[0],
            "contribution": row[1],
            "spend": row[2],
            "roas": row[3],
        })


# Read model metrics
model_metrics = {}

for row in metrics_ws.iter_rows(
    min_row=2,
    values_only=True
):
    if row[0] is not None:
        model_metrics[str(row[0]).lower()] = row[1]


# ---------------------------------------------------------
# 4. DASHBOARD DESIGN
# ---------------------------------------------------------

# Theme colours
NAVY = "142D4E"
BLUE = "2878B5"
LIGHT_BLUE = "EAF3F8"
WHITE = "FFFFFF"
DARK = "263445"
GREY = "68788A"
LIGHT_GREY = "F2F5F8"
GREEN = "198754"
ORANGE = "F0A43A"

thin_grey = Side(
    style="thin",
    color="D9E1E8"
)

# Worksheet layout
ws.sheet_view.showGridLines = False
ws.freeze_panes = "A5"

for col in range(1, 15):
    ws.column_dimensions[get_column_letter(col)].width = 13

ws.column_dimensions["A"].width = 18
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 16
ws.column_dimensions["D"].width = 14
ws.column_dimensions["E"].width = 4
ws.column_dimensions["F"].width = 15
ws.column_dimensions["G"].width = 15
ws.column_dimensions["H"].width = 15
ws.column_dimensions["I"].width = 4
ws.column_dimensions["J"].width = 15
ws.column_dimensions["K"].width = 15
ws.column_dimensions["L"].width = 15
ws.column_dimensions["M"].width = 15
ws.column_dimensions["N"].width = 15


# ---------------------------------------------------------
# 5. DASHBOARD TITLE
# ---------------------------------------------------------

ws.merge_cells("A1:N2")

title_cell = ws["A1"]
title_cell.value = "MARKETING PERFORMANCE DASHBOARD"
title_cell.font = Font(
    name="Arial",
    size=22,
    bold=True,
    color=WHITE
)
title_cell.fill = PatternFill(
    "solid",
    fgColor=NAVY
)
title_cell.alignment = Alignment(
    horizontal="center",
    vertical="center"
)

ws.row_dimensions[1].height = 28
ws.row_dimensions[2].height = 18

ws.merge_cells("A3:N3")
ws["A3"] = (
    "Marketing Mix Modelling | Revenue, Channel Performance "
    "and Predictive Analytics"
)
ws["A3"].font = Font(
    name="Arial",
    size=10,
    italic=True,
    color=GREY
)
ws["A3"].alignment = Alignment(
    horizontal="center"
)


# ---------------------------------------------------------
# 6. KPI CARDS
# ---------------------------------------------------------

def create_kpi_card(
    start_col,
    end_col,
    label,
    value,
    number_format=None
):
    label_row = 5
    value_row = 6

    start_letter = get_column_letter(start_col)
    end_letter = get_column_letter(end_col)

    ws.merge_cells(
        f"{start_letter}{label_row}:"
        f"{end_letter}{label_row}"
    )

    ws.merge_cells(
        f"{start_letter}{value_row}:"
        f"{end_letter}{value_row + 1}"
    )

    label_cell = ws.cell(
        row=label_row,
        column=start_col
    )

    value_cell = ws.cell(
        row=value_row,
        column=start_col
    )

    label_cell.value = label.upper()
    label_cell.font = Font(
        name="Arial",
        size=9,
        bold=True,
        color=GREY
    )
    label_cell.fill = PatternFill(
        "solid",
        fgColor=LIGHT_BLUE
    )
    label_cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    value_cell.value = value
    value_cell.font = Font(
        name="Arial",
        size=17,
        bold=True,
        color=NAVY
    )
    value_cell.fill = PatternFill(
        "solid",
        fgColor=LIGHT_BLUE
    )
    value_cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    if number_format:
        value_cell.number_format = number_format

    for row_num in range(label_row, value_row + 2):
        for col_num in range(start_col, end_col + 1):
            ws.cell(
                row=row_num,
                column=col_num
            ).border = Border(
                left=thin_grey,
                right=thin_grey,
                top=thin_grey,
                bottom=thin_grey
            )


create_kpi_card(
    1, 3,
    "Total Revenue",
    total_revenue,
    '£#,##0'
)

create_kpi_card(
    4, 6,
    "Average Weekly Revenue",
    average_revenue,
    '£#,##0'
)

create_kpi_card(
    7, 9,
    "Advertising Spend",
    total_spend,
    '£#,##0'
)

create_kpi_card(
    10, 12,
    "Estimated Marketing ROAS",
    overall_roas,
    '0.00x'
)

create_kpi_card(
    13, 14,
    "Weeks Analysed",
    weeks_analysed,
    '0'
)


ws.row_dimensions[5].height = 24
ws.row_dimensions[6].height = 28
ws.row_dimensions[7].height = 22


# ---------------------------------------------------------
# 7. CHANNEL PERFORMANCE TABLE
# ---------------------------------------------------------

ws.merge_cells("A10:D10")
ws["A10"] = "CHANNEL PERFORMANCE"
ws["A10"].font = Font(
    size=12,
    bold=True,
    color=WHITE
)
ws["A10"].fill = PatternFill(
    "solid",
    fgColor=NAVY
)
ws["A10"].alignment = Alignment(
    horizontal="center"
)

headers = [
    "Channel",
    "Contribution (£)",
    "Spend (£)",
    "ROAS"
]

for col_num, header in enumerate(headers, start=1):
    cell = ws.cell(
        row=11,
        column=col_num
    )
    cell.value = header
    cell.font = Font(
        bold=True,
        color=WHITE,
        size=9
    )
    cell.fill = PatternFill(
        "solid",
        fgColor=BLUE
    )
    cell.alignment = Alignment(
        horizontal="center",
        wrap_text=True
    )

for row_num, channel in enumerate(channels, start=12):
    values = [
        channel["name"],
        channel["contribution"],
        channel["spend"],
        channel["roas"],
    ]

    for col_num, value in enumerate(values, start=1):
        cell = ws.cell(
            row=row_num,
            column=col_num
        )
        cell.value = value
        cell.font = Font(
            size=9,
            color=DARK
        )
        cell.alignment = Alignment(
            horizontal="center"
        )
        cell.border = Border(
            bottom=thin_grey
        )

        if col_num in (2, 3):
            cell.number_format = '£#,##0'

        if col_num == 4:
            cell.number_format = '0.00x'


# ---------------------------------------------------------
# 8. MODEL PERFORMANCE TABLE
# ---------------------------------------------------------

ws.merge_cells("F10:H10")
ws["F10"] = "MODEL PERFORMANCE"
ws["F10"].font = Font(
    size=12,
    bold=True,
    color=WHITE
)
ws["F10"].fill = PatternFill(
    "solid",
    fgColor=NAVY
)
ws["F10"].alignment = Alignment(
    horizontal="center"
)

for col_num, header in enumerate(
    ["Metric", "Value"],
    start=6
):
    cell = ws.cell(
        row=11,
        column=col_num
    )
    cell.value = header
    cell.font = Font(
        bold=True,
        color=WHITE,
        size=9
    )
    cell.fill = PatternFill(
        "solid",
        fgColor=BLUE
    )
    cell.alignment = Alignment(
        horizontal="center"
    )

metric_labels = [
    ("MAE", "mae"),
    ("RMSE", "rmse"),
    ("R² Score", "r2"),
    ("Best Ridge Alpha", "best alpha"),
]

for row_num, (display_name, search_key) in enumerate(
    metric_labels,
    start=12
):
    value = None

    for key, metric_value in model_metrics.items():
        if search_key in key:
            value = metric_value
            break

    ws.cell(
        row=row_num,
        column=6
    ).value = display_name

    ws.cell(
        row=row_num,
        column=7
    ).value = value

    for col_num in (6, 7):
        cell = ws.cell(
            row=row_num,
            column=col_num
        )
        cell.font = Font(
            size=9,
            color=DARK
        )
        cell.alignment = Alignment(
            horizontal="center"
        )
        cell.border = Border(
            bottom=thin_grey
        )

    if display_name in ("MAE", "RMSE") and value is not None:
        ws.cell(
            row=row_num,
            column=7
        ).number_format = '£#,##0.00'

    elif display_name == "R² Score" and value is not None:
        ws.cell(
            row=row_num,
            column=7
        ).number_format = '0.0000'


# ---------------------------------------------------------
# 9. CHANNEL ROAS CHART
# ---------------------------------------------------------

if channels:
    roas_chart = BarChart()

    roas_chart.type = "bar"
    roas_chart.style = 10
    roas_chart.title = "Return on Advertising Spend by Channel"
    roas_chart.y_axis.title = "Marketing Channel"
    roas_chart.x_axis.title = "ROAS"
    roas_chart.height = 8
    roas_chart.width = 15
    roas_chart.legend = None

    data = Reference(
        ws,
        min_col=4,
        min_row=11,
        max_row=11 + len(channels)
    )

    categories = Reference(
        ws,
        min_col=1,
        min_row=12,
        max_row=11 + len(channels)
    )

    roas_chart.add_data(
        data,
        titles_from_data=True
    )
    roas_chart.set_categories(categories)

    roas_chart.dataLabels = DataLabelList()
    roas_chart.dataLabels.showVal = True

    ws.add_chart(
        roas_chart,
        "J10"
    )


# ---------------------------------------------------------
# 10. MONTHLY REVENUE TREND CHART
# ---------------------------------------------------------

monthly_last_row = monthly_ws.max_row

if monthly_last_row >= 3:
    monthly_chart = LineChart()

    monthly_chart.title = "Monthly Revenue Trend"
    monthly_chart.style = 13
    monthly_chart.y_axis.title = "Revenue (£)"
    monthly_chart.x_axis.title = "Month"
    monthly_chart.height = 9
    monthly_chart.width = 16
    monthly_chart.legend = None

    monthly_data = Reference(
        monthly_ws,
        min_col=2,
        min_row=1,
        max_row=monthly_last_row
    )

    monthly_categories = Reference(
        monthly_ws,
        min_col=1,
        min_row=2,
        max_row=monthly_last_row
    )

    monthly_chart.add_data(
        monthly_data,
        titles_from_data=True
    )
    monthly_chart.set_categories(
        monthly_categories
    )

    monthly_chart.dataLabels = DataLabelList()
    monthly_chart.dataLabels.showVal = False

    ws.add_chart(
        monthly_chart,
        "A20"
    )


# ---------------------------------------------------------
# 11. QUARTERLY REVENUE CHART
# ---------------------------------------------------------

quarterly_last_row = quarterly_ws.max_row

if quarterly_last_row >= 3:
    quarterly_chart = BarChart()

    quarterly_chart.type = "col"
    quarterly_chart.style = 11
    quarterly_chart.title = "Quarterly Revenue Performance"
    quarterly_chart.y_axis.title = "Revenue (£)"
    quarterly_chart.x_axis.title = "Quarter"
    quarterly_chart.height = 9
    quarterly_chart.width = 16
    quarterly_chart.legend = None

    quarterly_data = Reference(
        quarterly_ws,
        min_col=2,
        min_row=1,
        max_row=quarterly_last_row
    )

    quarterly_categories = Reference(
        quarterly_ws,
        min_col=1,
        min_row=2,
        max_row=quarterly_last_row
    )

    quarterly_chart.add_data(
        quarterly_data,
        titles_from_data=True
    )
    quarterly_chart.set_categories(
        quarterly_categories
    )

    quarterly_chart.dataLabels = DataLabelList()
    quarterly_chart.dataLabels.showVal = True

    ws.add_chart(
        quarterly_chart,
        "J27"
    )


# ---------------------------------------------------------
# 12. DASHBOARD FORMATTING
# ---------------------------------------------------------

for row_num in range(1, 45):
    if ws.row_dimensions[row_num].height is None:
        ws.row_dimensions[row_num].height = 21

# Section headings
for cell_range in ["A10:D10", "F10:H10"]:
    for row in ws[cell_range]:
        for cell in row:
            cell.fill = PatternFill(
                "solid",
                fgColor=NAVY
            )

# Dashboard footer
ws.merge_cells("A45:N45")
ws["A45"] = (
    "Note: This report uses model-estimated marketing "
    "contributions. ROAS estimates are not proof of causal "
    "incremental marketing impact."
)
ws["A45"].font = Font(
    size=9,
    italic=True,
    color=GREY
)
ws["A45"].alignment = Alignment(
    horizontal="center",
    vertical="center",
    wrap_text=True
)
ws.row_dimensions[45].height = 32


# ---------------------------------------------------------
# 13. PRINT AND VIEW SETTINGS
# ---------------------------------------------------------

ws.sheet_properties.pageSetUpPr.fitToPage = True

ws.page_setup.orientation = "landscape"
ws.page_setup.paperSize = ws.PAPERSIZE_A3
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 1

ws.print_area = "A1:N45"

ws.sheet_view.zoomScale = 85


# ---------------------------------------------------------
# 14. SAVE DASHBOARD
# ---------------------------------------------------------

try:
    wb.save(REPORT_PATH)

    print("\n" + "=" * 55)
    print("MARKETING DASHBOARD CREATED SUCCESSFULLY!")
    print("=" * 55)

    print(f"\nExcel report: {REPORT_PATH}")
    print("\nDashboard includes:")
    print("1. Total Revenue KPI")
    print("2. Average Weekly Revenue KPI")
    print("3. Advertising Spend KPI")
    print("4. Estimated Marketing ROAS KPI")
    print("5. Channel Performance Table")
    print("6. Model Performance Metrics")
    print("7. Channel ROAS Chart")
    print("8. Monthly Revenue Trend Chart")
    print("9. Quarterly Revenue Chart")

    print("\nOpen Marketing_Performance_Report.xlsx")
    print("and select the Dashboard worksheet.")

except PermissionError:
    print(
        "\nERROR: Excel file is currently open. "
        "Close the workbook and run this script again."
    )
