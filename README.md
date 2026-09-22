# Nassau Candy — Shipping Intelligence Command Center

A production-style Streamlit analytics dashboard for the Nassau Candy Distributor e-commerce shipping project.

## Included
- Executive Overview
- Network & Routes
- Operations Control Tower
- Commercial Intelligence
- Order Explorer
- Data Quality & Trust Center
- Global filters and reset control
- Interactive US destination map
- Factory → Region Sankey flow
- Route economics and leaderboard
- Product portfolio analysis
- Filtered route CSV export

## Required data file
Place the supplied dataset beside `app.py` using this exact filename:

`Nassau_Candy_Project_Final.csv`

## Run locally

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy
Push `app.py`, `requirements.txt`, `.streamlit/config.toml`, `README.md`, and the CSV to the GitHub repository. Deploy the repository with Streamlit Community Cloud using `app.py` as the entry point.

## Data-quality boundary
The supplied Order Date and Ship Date fields contain a systematic multi-year offset. The application therefore avoids presenting raw date differences as verified transit-time or delay KPIs. Volume, sales, profit, product, factory, destination, region and ship-mode analyses remain available.
