from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, ListFlowable, ListItem, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from ai_engine import generate_kpis, predict_sales

# ===============================
# LOAD DATA
# ===============================

df = pd.read_csv("clean_data.csv")
df.columns = df.columns.str.strip()

doc = SimpleDocTemplate("Executive_Report.pdf", pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# ===============================
# COMPANY LOGO
# ===============================

try:
    logo = Image("logo.png", width=2*inch, height=1*inch)
    elements.append(logo)
except:
    pass

elements.append(Spacer(1, 20))

# ===============================
# TITLE SECTION
# ===============================

elements.append(Paragraph(
    "AI-Driven Sales Performance Intelligence Report",
    styles["Title"]
))
elements.append(Spacer(1, 10))

elements.append(Paragraph(
    f"Generated On: {datetime.now().strftime('%d %B %Y')}",
    styles["Normal"]
))
elements.append(Spacer(1, 30))

# ===============================
# KPI SUMMARY
# ===============================

elements.append(Paragraph("1. Executive KPI Summary", styles["Heading2"]))
elements.append(Spacer(1, 10))

kpis = generate_kpis()

for key, value in kpis.items():
    elements.append(Paragraph(f"{key}: {value}", styles["Normal"]))
    elements.append(Spacer(1, 6))

elements.append(Spacer(1, 25))

# ===============================
# REGION PERFORMANCE CHART
# ===============================

elements.append(Paragraph("2. Regional Sales Distribution", styles["Heading2"]))
elements.append(Spacer(1, 10))

region_sales = df.groupby("Region")["Sum of Sales"].sum()
plt.figure()
region_sales.plot(kind="bar")
plt.title("Sales by Region")
plt.tight_layout()
plt.savefig("region_chart.png")
plt.close()

elements.append(Image("region_chart.png", width=5*inch, height=3*inch))
elements.append(Spacer(1, 25))

# ===============================
# CATEGORY PERFORMANCE CHART
# ===============================

elements.append(Paragraph("3. Category Performance", styles["Heading2"]))
elements.append(Spacer(1, 10))

category_sales = df.groupby("Category")["Sum of Sales"].sum()
plt.figure()
category_sales.plot(kind="pie", autopct='%1.1f%%')
plt.title("Category Sales Distribution")
plt.tight_layout()
plt.savefig("category_chart.png")
plt.close()

elements.append(Image("category_chart.png", width=5*inch, height=3*inch))
elements.append(Spacer(1, 25))

# ===============================
# FORECAST SECTION
# ===============================

elements.append(Paragraph("4. Sales Forecast", styles["Heading2"]))
elements.append(Spacer(1, 10))

predicted_sales = predict_sales()
elements.append(Paragraph(
    f"Predicted Next Month Sales: {predicted_sales:,.2f}",
    styles["Normal"]
))
elements.append(Spacer(1, 20))

# ===============================
# RISK ANALYSIS
# ===============================

elements.append(Paragraph("5. Risk & Profitability Analysis", styles["Heading2"]))
elements.append(Spacer(1, 10))

loss_products = df[df["Sum of Profit"] < 0]
elements.append(Paragraph(
    f"Number of Loss-Making Products: {len(loss_products)}",
    styles["Normal"]
))
elements.append(Spacer(1, 20))

# ===============================
# DYNAMIC BUSINESS RECOMMENDATIONS
# ===============================

elements.append(Paragraph("6. Strategic Recommendations", styles["Heading2"]))
elements.append(Spacer(1, 10))

total_profit = df["Sum of Profit"].sum()
profit_margin = (df["Sum of Profit"].sum() / df["Sum of Sales"].sum()) * 100

recommendations = []

if profit_margin < 10:
    recommendations.append("Improve pricing strategy to increase overall profit margin.")

if len(loss_products) > 0:
    recommendations.append("Review loss-making products and optimize cost structure.")

best_region = region_sales.idxmax()
recommendations.append(f"Focus expansion strategies in high-performing region: {best_region}.")

if predicted_sales > df["Sum of Sales"].mean():
    recommendations.append("Forecast indicates growth potential. Increase inventory planning.")

elements.append(ListFlowable(
    [ListItem(Paragraph(r, styles["Normal"])) for r in recommendations],
    bulletType='bullet'
))

elements.append(Spacer(1, 30))

# ===============================
# CONCLUSION
# ===============================

elements.append(Paragraph("7. Executive Conclusion", styles["Heading2"]))
elements.append(Spacer(1, 10))

elements.append(Paragraph(
    "This AI-powered Business Intelligence system integrates dashboard analytics, "
    "risk assessment, and predictive forecasting to support strategic decision-making.",
    styles["Normal"]
))

# ===============================
# BUILD DOCUMENT
# ===============================

doc.build(elements)

print("Executive Report Generated Successfully")