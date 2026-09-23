# 🍫 Nassau Candy — Shipping Intelligence Command Center

## 📊 Data Science | E-Commerce Analytics

A production-style Streamlit analytics dashboard for the Nassau Candy Distributor e-commerce shipping project.

The dashboard provides a centralized view of distribution concentration, factory contribution, route economics, product demand, shipping patterns, and order-level shipment information.

## 🌐 Live Dashboard

👉 https://bupju4c3a7bgbpmaw47sbz.streamlit.app/

## 💻 GitHub Repository

👉 https://github.com/birajdarsanika717-dyp/Nassau-Candy-Shipping-Intelligence

---

## 🎯 Project Objective

The project analyzes factory-to-customer shipping data to understand:

- Distribution and destination concentration
- Factory contribution
- Factory-to-state route patterns
- Route-level sales and profit
- Shipping-mode utilization
- Product demand and commercial contribution
- Order-level shipment details

## 📈 Dashboard Features

### Executive Overview
High-level shipment, units, sales, gross profit, margin, destination, factory, product, and shipping-mode insights.

### Network & Route Intelligence
- Interactive US destination map
- Factory → State route analysis
- Route economics
- Route leaderboard
- Shipment concentration analysis

### Operations Control Tower
- Shipping-mode utilization
- Regional shipment mix
- Factory → Region Sankey flow
- Factory performance

### Commercial Intelligence
- Top products by shipment volume
- Product sales and profit contribution
- Product portfolio analysis

### Order Explorer
- Factory and destination filters
- Route KPIs
- Shipping-mode performance
- Product performance
- Order-level shipment records
- Filtered route CSV export

### Data Quality & Trust Center
- Dataset completeness checks
- Duplicate validation
- Date-range validation
- Data-quality limitations
- Transparent methodology

## ⚠️ Data Quality Note

The supplied Order Date and Ship Date fields contain a systematic multi-year offset.

Therefore, calculated lead-time values are **not treated as verified real-world transit or delay metrics**.

Volume, sales, profit, product, factory, and geographic analyses are used as the reliable business-analysis layer until the source dates can be validated.

## 🛠️ Technologies

- Python
- Pandas
- Plotly
- Streamlit
- Git
- GitHub

## 📁 Project Structure

```text
Nassau-Candy-Shipping-Intelligence/
│
├── app.py
├── Nassau_Candy_Project_Final.csv
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml