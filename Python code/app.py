import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from ai_engine import generate_kpis, detect_anomalies, predict_sales

st.set_page_config(page_title="AI BI Assistant", layout="wide")

st.title("AI-Powered Sales Business Intelligence Dashboard")

# Load dataset
df = pd.read_csv("clean_data.csv")
df.columns = df.columns.str.strip()

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Executive Overview",
        "Sales Analytics",
        "Risk & Performance",
        "AI Insights",
        "Ask Question",
        "Generate Report"
    ]
)

# ------------------- EXECUTIVE OVERVIEW -------------------
if menu == "Executive Overview":

    kpis = generate_kpis()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"{kpis['Total Sales']:.2f}")
    col2.metric("Total Profit", f"{kpis['Total Profit']:.2f}")
    col3.metric("Total Orders", kpis['Total Orders'])
    col4.metric("Best Region", kpis['Best Region'])

    st.markdown("---")

    # Sales by Region Chart
    st.subheader("Sales by Region")
    region_sales = df.groupby("Region")["Sum of Sales"].sum()
    st.bar_chart(region_sales)


# ------------------- SALES ANALYTICS -------------------
elif menu == "Sales Analytics":

    st.subheader("Category Sales Distribution")
    category_sales = df.groupby("Category")["Sum of Sales"].sum()
    st.bar_chart(category_sales)

    st.subheader("Monthly Sales Trend")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    monthly_sales = df.groupby(df['Order Date'].dt.to_period("M"))["Sum of Sales"].sum()
    monthly_sales.index = monthly_sales.index.astype(str)
    st.line_chart(monthly_sales)

    st.subheader("Top 10 Products")
    top_products = df.groupby("Product Name")["Sum of Sales"].sum().sort_values(ascending=False).head(10)
    st.dataframe(top_products)


# ------------------- RISK & PERFORMANCE -------------------
elif menu == "Risk & Performance":

    st.subheader("Low Profit Products (Risk Area)")
    low_profit = df[df["Sum of Profit"] < 0]
    st.dataframe(low_profit[["Product Name", "Region", "Sum of Profit"]])

    st.subheader("Profit Margin Analysis")
    df["Profit Margin"] = df["Sum of Profit"] / df["Sum of Sales"]
    margin_by_region = df.groupby("Region")["Profit Margin"].mean()
    st.bar_chart(margin_by_region)

    st.subheader("High Discount Impact")
    if "Discount" in df.columns:
        discount_impact = df.groupby("Discount")["Sum of Profit"].mean()
        st.line_chart(discount_impact)


# ------------------- AI INSIGHTS -------------------
elif menu == "AI Insights":

    st.subheader("Sales Forecast")
    prediction = predict_sales()
    st.success(f"Next Month Predicted Sales: {prediction:.2f}")

    st.subheader("Anomaly Detection")
    anomalies = detect_anomalies()
    st.dataframe(anomalies)

    st.info("AI Engine uses predictive modeling and anomaly detection for decision support.")


# ------------------- CHATBOT -------------------
elif menu == "Ask Question":
    st.subheader("AI Business Intelligence Assistant")

    question = st.text_input("Ask any business question about sales, profit, region, product, trends, risk, customers...")

    if question:
        df = pd.read_csv("clean_data.csv")
        df.columns = df.columns.str.strip()

        q = question.lower()

        total_sales = df["Sum of Sales"].sum()
        total_profit = df["Sum of Profit"].sum()
        total_orders = df["Order ID"].nunique()

        # =============================
        # EXECUTIVE KPI QUESTIONS
        # =============================

        if "total sales" in q:
            st.success(f"Total Sales: {total_sales:,.2f}")

        elif "total profit" in q:
            st.success(f"Total Profit: {total_profit:,.2f}")

        elif "total orders" in q:
            st.success(f"Total Orders: {total_orders}")

        elif "average order value" in q:
            aov = total_sales / total_orders
            st.success(f"Average Order Value: {aov:,.2f}")

        elif "profit margin" in q:
            margin = (total_profit / total_sales) * 100
            st.success(f"Overall Profit Margin: {margin:.2f}%")

        # =============================
        # REGION ANALYSIS
        # =============================

        elif "region performance" in q:
            region_sales = df.groupby("Region")["Sum of Sales"].sum().sort_values(ascending=False)
            st.bar_chart(region_sales)

        elif "best region" in q:
            best = df.groupby("Region")["Sum of Sales"].sum().idxmax()
            st.success(f"Best Region: {best}")

        elif "worst region" in q:
            worst = df.groupby("Region")["Sum of Sales"].sum().idxmin()
            st.success(f"Worst Region: {worst}")

        elif "region profit comparison" in q:
            region_profit = df.groupby("Region")["Sum of Profit"].sum()
            st.bar_chart(region_profit)

        # =============================
        # CATEGORY ANALYSIS
        # =============================

        elif "category comparison" in q:
            cat = df.groupby("Category")["Sum of Sales"].sum()
            st.bar_chart(cat)

        elif "most profitable category" in q:
            cat_profit = df.groupby("Category")["Sum of Profit"].sum().idxmax()
            st.success(f"Most Profitable Category: {cat_profit}")

        elif "least profitable category" in q:
            cat_profit = df.groupby("Category")["Sum of Profit"].sum().idxmin()
            st.success(f"Least Profitable Category: {cat_profit}")

        # =============================
        # PRODUCT ANALYSIS
        # =============================

        elif "top 10 products" in q:
            top_products = df.groupby("Product Name")["Sum of Sales"].sum().sort_values(ascending=False).head(10)
            st.bar_chart(top_products)

        elif "low performing products" in q:
            low_products = df.groupby("Product Name")["Sum of Sales"].sum().sort_values().head(10)
            st.bar_chart(low_products)

        elif "highest profit product" in q:
            prod = df.groupby("Product Name")["Sum of Profit"].sum().idxmax()
            st.success(f"Highest Profit Product: {prod}")

        # =============================
        # CUSTOMER ANALYSIS
        # =============================

        elif "top 5 customers" in q:
            customers = df.groupby("Customer Name")["Sum of Sales"].sum().sort_values(ascending=False).head(5)
            st.bar_chart(customers)

        elif "customer segmentation" in q:
            seg = df.groupby("Segment")["Sum of Sales"].sum()
            st.pie_chart(seg)

        # =============================
        # TIME ANALYSIS
        # =============================

        elif "monthly trend" in q:
            monthly = df.groupby("Month")["Sum of Sales"].sum()
            st.line_chart(monthly)

        elif "yearly growth" in q:
            yearly = df.groupby("Year")["Sum of Sales"].sum()
            growth = yearly.pct_change() * 100
            st.line_chart(growth)

        elif "best month" in q:
            best_month = df.groupby("Month")["Sum of Sales"].sum().idxmax()
            st.success(f"Best Performing Month: {best_month}")

        # =============================
        # RISK & PERFORMANCE
        # =============================

        elif "loss making products" in q:
            loss_products = df[df["Sum of Profit"] < 0]
            st.dataframe(loss_products)

        elif "declining trend" in q:
            monthly = df.groupby("Month")["Sum of Sales"].sum()
            decline = monthly.pct_change()
            st.line_chart(monthly)
            st.write("Percentage Change")
            st.write(decline)

        elif "high discount impact" in q:
            discount_effect = df.groupby("Discount")["Sum of Profit"].mean()
            st.line_chart(discount_effect)

        # =============================
        # COMPARISON QUESTIONS
        # =============================

        elif "compare sales and profit" in q:
            compare = df.groupby("Month")[["Sum of Sales", "Sum of Profit"]].sum()
            st.line_chart(compare)

        elif "sales vs orders" in q:
            orders = df.groupby("Month")["Order ID"].nunique()
            sales = df.groupby("Month")["Sum of Sales"].sum()
            st.line_chart(pd.DataFrame({"Sales": sales, "Orders": orders}))

        # =============================
        # BUSINESS INSIGHT SUMMARY
        # =============================

        elif "business insight" in q or "overall analysis" in q:
            best_region = df.groupby("Region")["Sum of Sales"].sum().idxmax()
            best_category = df.groupby("Category")["Sum of Sales"].sum().idxmax()
            st.info(f"""
            Business Insight Summary:
            • Total Sales: {total_sales:,.2f}
            • Total Profit: {total_profit:,.2f}
            • Best Region: {best_region}
            • Best Category: {best_category}
            • Overall Business is {'Profitable' if total_profit > 0 else 'Under Risk'}
            """)

        else:
            st.warning("Try asking about KPIs, region performance, product ranking, trends, risk analysis, growth, comparison, customers, or overall business insight.")


# ------------------- Generate Report -------------------
elif menu == "Generate Report":

    st.header("📄 Executive Report Generator")

    st.markdown("""
    This module generates a AI-driven executive report including:

    • Executive KPI Summary  
    • Regional & Category Performance Charts  
    • Forecast Analysis  
    • Risk & Profitability Insights  
    • Strategic Business Recommendations  
    """)

    if st.button("Generate Full Executive PDF Report"):

        with st.spinner("Generating Executive Report... Please wait."):

            try:
                subprocess.run(["python", "report_generator.py"], check=True)

                st.success("Executive_Report.pdf Generated Successfully!")

                with open("Executive_Report.pdf", "rb") as file:
                    st.download_button(
                        label="📥 Download Executive Report",
                        data=file,
                        file_name="Executive_Report.pdf",
                        mime="application/pdf"
                    )

            except subprocess.CalledProcessError:
                st.error("Report generation failed. Please check report_generator.py.")