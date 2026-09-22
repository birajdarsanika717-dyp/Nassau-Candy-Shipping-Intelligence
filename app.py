import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# NASSAU CANDY | EXECUTIVE SHIPPING INTELLIGENCE
# Production-style Streamlit single-page application
# ============================================================

st.set_page_config(
    page_title="Nassau Candy | Shipping Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Design system
# -----------------------------
st.markdown(
    """
    <style>
    :root {
        --ink: #0f172a;
        --muted: #64748b;
        --line: #e2e8f0;
        --panel: #ffffff;
        --soft: #f8fafc;
        --brand: #2563eb;
        --brand-dark: #1e3a8a;
        --good: #15803d;
        --warn: #b45309;
        --danger: #b91c1c;
    }

    .stApp { background: #f6f8fb; color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(246,248,251,.88); }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #172554 58%, #2563eb 100%);
        color: white; border-radius: 20px; padding: 28px 32px;
        margin-bottom: 18px; box-shadow: 0 14px 35px rgba(15,23,42,.14);
    }
    .hero .eyebrow { font-size: .76rem; letter-spacing: .14em; text-transform: uppercase; opacity: .72; font-weight: 700; }
    .hero h1 { margin: 6px 0 8px 0; font-size: 2.15rem; line-height: 1.1; }
    .hero p { margin: 0; color: #dbeafe; max-width: 900px; font-size: 1rem; }

    .section-head { margin: 22px 0 10px 0; }
    .section-head h2 { margin: 0; color: var(--ink); font-size: 1.35rem; }
    .section-head p { margin: 3px 0 0 0; color: var(--muted); font-size: .9rem; }

    .insight {
        background: white; border: 1px solid var(--line); border-radius: 14px;
        padding: 16px 18px; min-height: 126px; box-shadow: 0 4px 14px rgba(15,23,42,.04);
    }
    .insight .label { color: var(--muted); font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; }
    .insight .value { color: var(--ink); font-size: 1.18rem; font-weight: 800; margin: 7px 0 4px; }
    .insight .detail { color: var(--muted); font-size: .86rem; line-height: 1.4; }

    .trust {
        border-left: 4px solid #d97706; background: #fffbeb; padding: 13px 16px;
        border-radius: 10px; color: #78350f; margin: 10px 0 18px;
    }
    .trust strong { color: #92400e; }

    .status {
        display: inline-flex; align-items: center; gap: 7px; background: #ecfdf5;
        color: #166534; border: 1px solid #bbf7d0; border-radius: 999px;
        padding: 5px 10px; font-size: .76rem; font-weight: 700;
    }
    .status-dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; }

    .metric-note { color: var(--muted); font-size: .74rem; margin-top: -8px; }
    .footer { color: #94a3b8; text-align: center; padding: 24px 0 8px; font-size: .78rem; }

    .block-container { padding-top: 1.1rem; padding-bottom: 2rem; }
    div[data-testid="stMetric"] { background: white; border: 1px solid var(--line); padding: 15px 16px; border-radius: 14px; box-shadow: 0 4px 14px rgba(15,23,42,.04); }
    div[data-testid="stMetricLabel"] { color: var(--muted); }
    div[data-testid="stMetricValue"] { color: var(--ink); }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] { border-radius: 9px; padding: 8px 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Data loading
# -----------------------------
@st.cache_data

def load_data():
    df = pd.read_csv("Nassau_Candy_Project_Final.csv")

    # The source contains mixed date formats. Keep parsing robust and explicit.
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], format="mixed", dayfirst=True, errors="coerce"
    )
    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"], format="mixed", dayfirst=False, errors="coerce"
    )

    # Safe business metrics. Do NOT treat Shipping Lead Time as verified transit time.
    if "Factory" not in df.columns:
        factory_mapping = {
            "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
            "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
            "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
            "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
            "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
            "Laffy Taffy": "Sugar Shack",
            "SweeTARTS": "Sugar Shack",
            "Nerds": "Sugar Shack",
            "Fun Dip": "Sugar Shack",
            "Fizzy Lifting Drinks": "Sugar Shack",
            "Everlasting Gobstopper": "Secret Factory",
            "Lickable Wallpaper": "Secret Factory",
            "Wonka Gum": "Secret Factory",
            "Hair Toffee": "The Other Factory",
            "Kazookles": "The Other Factory",
        }
        df["Factory"] = df["Product Name"].map(factory_mapping)

    if "Route" not in df.columns:
        df["Route"] = df["Factory"] + " → " + df["State/Province"]

    df["Profit Margin %"] = (df["Gross Profit"] / df["Sales"].replace(0, pd.NA) * 100).fillna(0)
    return df


df = load_data()

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Nassau Candy Distributor · E-commerce Analytics</div>
      <h1>Shipping Intelligence Command Center</h1>
      <p>One operating view for understanding distribution concentration, factory contribution, route economics, product demand and shipment patterns — without forcing the client to hunt through disconnected charts.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar: global control center
# -----------------------------
st.sidebar.markdown("## Control Center")
st.sidebar.caption("Use these controls to change every view at once.")

with st.sidebar:
    if st.button("↺ Reset all filters", use_container_width=True):
        for key in ["factory_filter", "state_filter", "region_filter", "mode_filter", "product_filter"]:
            st.session_state.pop(key, None)
        st.rerun()

    factory_options = sorted(df["Factory"].dropna().unique())
    state_options = sorted(df["State/Province"].dropna().unique())
    region_options = sorted(df["Region"].dropna().unique())
    mode_options = sorted(df["Ship Mode"].dropna().unique())
    product_options = sorted(df["Product Name"].dropna().unique())

    selected_factory = st.multiselect("Factory", factory_options, default=factory_options, key="factory_filter")
    selected_state = st.multiselect("Destination", state_options, default=state_options, key="state_filter")
    selected_region = st.multiselect("Region", region_options, default=region_options, key="region_filter")
    selected_mode = st.multiselect("Ship mode", mode_options, default=mode_options, key="mode_filter")
    selected_product = st.multiselect("Product", product_options, default=product_options, key="product_filter")

    st.divider()
    st.markdown("**Current dataset**")
    st.caption(f"{len(df):,} shipment records")
    st.caption(f"{df['Order Date'].min():%d %b %Y} → {df['Order Date'].max():%d %b %Y} order dates")
    st.markdown('<div class="status"><span class="status-dot"></span>Dashboard operational</div>', unsafe_allow_html=True)

filtered_df = df[
    df["Factory"].isin(selected_factory)
    & df["State/Province"].isin(selected_state)
    & df["Region"].isin(selected_region)
    & df["Ship Mode"].isin(selected_mode)
    & df["Product Name"].isin(selected_product)
].copy()

if filtered_df.empty:
    st.error("No records match the current filter combination. Use Reset all filters in the Control Center.")
    st.stop()

# -----------------------------
# Trust boundary / data quality
# -----------------------------
st.markdown(
    """
    <div class="trust"><strong>Data-quality boundary:</strong> The supplied Order Date and Ship Date fields contain a systematic multi-year offset. Volume, sales, profit, product, factory and geographic analyses are therefore presented as the reliable business layer. Lead-time values are deliberately <strong>not</strong> used as verified real-world transit or delay metrics until the source dates are validated.</div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# KPI strip
# -----------------------------
total_shipments = len(filtered_df)
total_units = int(filtered_df["Units"].sum())
total_sales = float(filtered_df["Sales"].sum())
total_profit = float(filtered_df["Gross Profit"].sum())
margin = total_profit / total_sales * 100 if total_sales else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Shipments", f"{total_shipments:,}")
k2.metric("Units", f"{total_units:,}")
k3.metric("Sales", f"${total_sales:,.2f}")
k4.metric("Gross Profit", f"${total_profit:,.2f}")
k5.metric("Profit Margin", f"{margin:.1f}%")

st.markdown('<div class="metric-note">All KPI values respond to the global filters.</div>', unsafe_allow_html=True)

# -----------------------------
# Helper functions
# -----------------------------
def money(x):
    return f"${x:,.2f}"


def add_common_layout(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, Arial, sans-serif", color="#0f172a"),
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eef2f7", zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


# -----------------------------
# Navigation ecosystem
# -----------------------------
tab_overview, tab_network, tab_operations, tab_commercial, tab_orders, tab_quality = st.tabs(
    ["Executive Overview", "Network & Routes", "Operations", "Commercial", "Order Explorer", "Data Quality"]
)

# ============================================================
# TAB 1 — EXECUTIVE OVERVIEW
# ============================================================
with tab_overview:
    st.markdown('<div class="section-head"><h2>Executive Overview</h2><p>The first screen answers the questions a decision-maker usually asks first.</p></div>', unsafe_allow_html=True)

    state_summary = (
        filtered_df.groupby("State/Province")
        .agg(Shipments=("Order ID", "count"), Sales=("Sales", "sum"), Profit=("Gross Profit", "sum"))
        .reset_index().sort_values("Shipments", ascending=False)
    )
    factory_summary = (
        filtered_df.groupby("Factory")
        .agg(Shipments=("Order ID", "count"), Sales=("Sales", "sum"), Profit=("Gross Profit", "sum"))
        .reset_index().sort_values("Shipments", ascending=False)
    )
    product_summary = (
        filtered_df.groupby("Product Name")
        .agg(Shipments=("Order ID", "count"), Units=("Units", "sum"), Sales=("Sales", "sum"), Profit=("Gross Profit", "sum"))
        .reset_index().sort_values("Shipments", ascending=False)
    )
    mode_summary = filtered_df.groupby("Ship Mode").agg(Shipments=("Order ID", "count")).reset_index().sort_values("Shipments", ascending=False)

    top_state = state_summary.iloc[0]
    top_factory = factory_summary.iloc[0]
    top_product = product_summary.iloc[0]
    top_mode = mode_summary.iloc[0]

    a, b, c, d = st.columns(4)
    with a:
        st.markdown(f'<div class="insight"><div class="label">Highest-volume destination</div><div class="value">{top_state["State/Province"]}</div><div class="detail">{int(top_state["Shipments"]):,} shipments · {top_state["Shipments"] / total_shipments * 100:.1f}% of current volume</div></div>', unsafe_allow_html=True)
    with b:
        st.markdown(f'<div class="insight"><div class="label">Largest factory contribution</div><div class="value">{top_factory["Factory"]}</div><div class="detail">{int(top_factory["Shipments"]):,} shipments · {top_factory["Shipments"] / total_shipments * 100:.1f}% of current volume</div></div>', unsafe_allow_html=True)
    with c:
        st.markdown(f'<div class="insight"><div class="label">Highest-volume product</div><div class="value">{top_product["Product Name"]}</div><div class="detail">{int(top_product["Shipments"]):,} shipments · {int(top_product["Units"]):,} units</div></div>', unsafe_allow_html=True)
    with d:
        st.markdown(f'<div class="insight"><div class="label">Most-used shipping mode</div><div class="value">{top_mode["Ship Mode"]}</div><div class="detail">{int(top_mode["Shipments"]):,} shipments · {top_mode["Shipments"] / total_shipments * 100:.1f}% of current volume</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-head"><h2>Where the business is concentrated</h2><p>Concentration is shown by shipment volume, with sales and profit available on hover.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        top_states = state_summary.head(10).sort_values("Shipments")
        fig = px.bar(top_states, x="Shipments", y="State/Province", orientation="h", title="Top destinations by shipment volume", hover_data={"Sales":":$,.2f", "Profit":":$,.2f"})
        add_common_layout(fig, 420)
        st.plotly_chart(fig, width="stretch")
    with c2:
        top_factories = factory_summary.sort_values("Shipments")
        fig = px.bar(top_factories, x="Shipments", y="Factory", orientation="h", title="Factory contribution to shipment volume", hover_data={"Sales":":$,.2f", "Profit":":$,.2f"})
        add_common_layout(fig, 420)
        st.plotly_chart(fig, width="stretch")

    st.markdown('<div class="section-head"><h2>Management snapshot</h2><p>These are descriptive signals from the selected records, not predictive forecasts.</p></div>', unsafe_allow_html=True)
    snapshot = state_summary.head(8).copy()
    snapshot["Shipment Share %"] = snapshot["Shipments"] / total_shipments * 100
    snapshot["Profit Margin %"] = snapshot["Profit"] / snapshot["Sales"].replace(0, pd.NA) * 100
    snapshot = snapshot[["State/Province", "Shipments", "Shipment Share %", "Sales", "Profit", "Profit Margin %"]]
    st.dataframe(snapshot.style.format({"Shipment Share %":"{:.1f}", "Sales": "${:,.2f}", "Profit":"${:,.2f}", "Profit Margin %":"{:.1f}"}), width="stretch", hide_index=True)

# ============================================================
# TAB 2 — NETWORK & ROUTES
# ============================================================
with tab_network:
    st.markdown('<div class="section-head"><h2>Network & Route Intelligence</h2><p>Move from the national picture into factory-to-destination concentration and route economics.</p></div>', unsafe_allow_html=True)

    us_state_codes = {
        "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"
    }

    map_data = filtered_df.groupby("State/Province").agg(Shipments=("Order ID","count"), Sales=("Sales","sum"), Profit=("Gross Profit","sum")).reset_index()
    map_data["State Code"] = map_data["State/Province"].map(us_state_codes)
    map_data = map_data.dropna(subset=["State Code"])

    if not map_data.empty:
        fig = px.choropleth(map_data, locations="State Code", locationmode="USA-states", color="Shipments", scope="usa", hover_name="State/Province", hover_data={"Shipments":True,"Sales":":$,.2f","Profit":":$,.2f","State Code":False}, title="Destination concentration across the US")
        fig.update_layout(geo=dict(showlakes=True, lakecolor="white"))
        add_common_layout(fig, 500)
        st.plotly_chart(fig, width="stretch")

    route_summary = (
        filtered_df.groupby("Route")
        .agg(Shipments=("Order ID","count"), Units=("Units","sum"), Sales=("Sales","sum"), Profit=("Gross Profit","sum"))
        .reset_index()
    )
    route_summary["Profit Margin %"] = route_summary["Profit"] / route_summary["Sales"].replace(0,pd.NA) * 100
    route_summary["Shipment Share %"] = route_summary["Shipments"] / total_shipments * 100

    r1, r2 = st.columns(2)
    with r1:
        top_routes = route_summary.nlargest(10, "Shipments").sort_values("Shipments")
        fig = px.bar(top_routes, x="Shipments", y="Route", orientation="h", title="Top factory-to-state routes", hover_data={"Sales":":$,.2f","Profit":":$,.2f","Profit Margin %":":.1f"})
        add_common_layout(fig, 430)
        st.plotly_chart(fig, width="stretch")
    with r2:
        route_econ = route_summary.nlargest(12, "Sales").copy()
        fig = px.scatter(route_econ, x="Sales", y="Profit", size="Shipments", hover_name="Route", title="Route economics: sales vs gross profit", hover_data={"Shipments":True,"Profit Margin %":":.1f"})
        add_common_layout(fig, 430)
        st.plotly_chart(fig, width="stretch")

    st.markdown('<div class="section-head"><h2>Route leaderboard</h2><p>Operational proxy: volume and financial contribution. This deliberately avoids unsupported transit-time rankings.</p></div>', unsafe_allow_html=True)
    route_table = route_summary.sort_values(["Shipments","Profit"], ascending=False).head(20).copy()
    st.dataframe(route_table.style.format({"Sales":"${:,.2f}","Profit":"${:,.2f}","Profit Margin %":"{:.1f}","Shipment Share %":"{:.1f}"}), width="stretch", hide_index=True)

# ============================================================
# TAB 3 — OPERATIONS
# ============================================================
with tab_operations:
    st.markdown('<div class="section-head"><h2>Operations Control Tower</h2><p>Understand shipping-mode mix, factory utilization and the factory-to-region flow.</p></div>', unsafe_allow_html=True)

    o1, o2 = st.columns(2)
    with o1:
        mode = filtered_df.groupby("Ship Mode").agg(Shipments=("Order ID","count"), Sales=("Sales","sum"), Profit=("Gross Profit","sum")).reset_index()
        mode["Share %"] = mode["Shipments"] / total_shipments * 100
        fig = px.bar(mode.sort_values("Shipments"), x="Shipments", y="Ship Mode", orientation="h", title="Shipping mode utilization", hover_data={"Sales":":$,.2f","Profit":":$,.2f","Share %":":.1f"})
        add_common_layout(fig, 400)
        st.plotly_chart(fig, width="stretch")
    with o2:
        region = filtered_df.groupby("Region").agg(Shipments=("Order ID","count"), Sales=("Sales","sum"), Profit=("Gross Profit","sum")).reset_index()
        fig = px.bar(region.sort_values("Shipments"), x="Shipments", y="Region", orientation="h", title="Regional shipment mix", hover_data={"Sales":":$,.2f","Profit":":$,.2f"})
        add_common_layout(fig, 400)
        st.plotly_chart(fig, width="stretch")

    # Sankey factory -> region
    flow = filtered_df.groupby(["Factory","Region"]).size().reset_index(name="Shipments")
    labels = list(pd.unique(pd.concat([flow["Factory"], flow["Region"]], ignore_index=True)))
    idx = {v:i for i,v in enumerate(labels)}
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(label=labels, pad=18, thickness=18),
        link=dict(source=flow["Factory"].map(idx), target=flow["Region"].map(idx), value=flow["Shipments"]),
    ))
    fig.update_layout(title="Factory → Region shipment flow", height=480, margin=dict(l=10,r=10,t=55,b=10), paper_bgcolor="white")
    st.plotly_chart(fig, width="stretch")

    factory_ops = filtered_df.groupby("Factory").agg(Shipments=("Order ID","count"), Units=("Units","sum"), Sales=("Sales","sum"), Profit=("Gross Profit","sum")).reset_index()
    factory_ops["Share %"] = factory_ops["Shipments"] / total_shipments * 100
    factory_ops["Profit Margin %"] = factory_ops["Profit"] / factory_ops["Sales"].replace(0,pd.NA) * 100
    st.dataframe(factory_ops.sort_values("Shipments", ascending=False).style.format({"Sales":"${:,.2f}","Profit":"${:,.2f}","Share %":"{:.1f}","Profit Margin %":"{:.1f}"}), width="stretch", hide_index=True)

# ============================================================
# TAB 4 — COMMERCIAL
# ============================================================
with tab_commercial:
    st.markdown('<div class="section-head"><h2>Commercial Intelligence</h2><p>Connect product demand with sales and gross-profit contribution.</p></div>', unsafe_allow_html=True)

    prod = filtered_df.groupby("Product Name").agg(Shipments=("Order ID","count"), Units=("Units","sum"), Sales=("Sales","sum"), Profit=("Gross Profit","sum")).reset_index()
    prod["Profit Margin %"] = prod["Profit"] / prod["Sales"].replace(0,pd.NA) * 100
    prod["Sales Share %"] = prod["Sales"] / total_sales * 100

    p1, p2 = st.columns(2)
    with p1:
        top = prod.nlargest(10,"Shipments").sort_values("Shipments")
        fig = px.bar(top, x="Shipments", y="Product Name", orientation="h", title="Top products by shipment volume", hover_data={"Units":True,"Sales":":$,.2f","Profit":":$,.2f"})
        add_common_layout(fig, 450)
        st.plotly_chart(fig, width="stretch")
    with p2:
        top = prod.nlargest(10,"Sales")
        fig = px.treemap(top, path=["Product Name"], values="Sales", color="Profit", title="Sales concentration by product", hover_data={"Profit Margin %":":.1f"})
        add_common_layout(fig, 450)
        st.plotly_chart(fig, width="stretch")

    st.markdown('<div class="section-head"><h2>Product portfolio table</h2><p>Use this table to identify high-volume and high-value products without relying on a single ranking.</p></div>', unsafe_allow_html=True)
    st.dataframe(prod.sort_values("Sales", ascending=False).style.format({"Sales":"${:,.2f}","Profit":"${:,.2f}","Profit Margin %":"{:.1f}","Sales Share %":"{:.1f}"}), width="stretch", hide_index=True)

# ============================================================
# TAB 5 — ORDER EXPLORER
# ============================================================
with tab_orders:
    st.markdown('<div class="section-head"><h2>Order Explorer</h2><p>Drill from the selected factory and destination into the actual shipment records.</p></div>', unsafe_allow_html=True)

    available_factories = sorted(filtered_df["Factory"].dropna().unique())
    available_states = sorted(filtered_df["State/Province"].dropna().unique())
    oc1, oc2 = st.columns(2)
    with oc1:
        route_factory = st.selectbox("Factory", available_factories, key="explorer_factory")
    with oc2:
        route_state = st.selectbox("Destination state / province", available_states, key="explorer_state")

    route_df = filtered_df[(filtered_df["Factory"] == route_factory) & (filtered_df["State/Province"] == route_state)].copy()

    if route_df.empty:
        st.info("No records for this factory-destination combination.")
    else:
        rs1, rs2, rs3, rs4, rs5 = st.columns(5)
        route_sales = route_df["Sales"].sum(); route_profit = route_df["Gross Profit"].sum()
        rs1.metric("Shipments", f"{len(route_df):,}")
        rs2.metric("Units", f"{int(route_df['Units'].sum()):,}")
        rs3.metric("Sales", money(route_sales))
        rs4.metric("Profit", money(route_profit))
        rs5.metric("Margin", f"{route_profit / route_sales * 100:.1f}%" if route_sales else "0.0%")

        mode_route = route_df.groupby("Ship Mode").agg(Shipments=("Order ID","count"), Units=("Units","sum"), Sales=("Sales","sum"), Profit=("Gross Profit","sum")).reset_index()
        mode_route["Profit Margin %"] = mode_route["Profit"] / mode_route["Sales"].replace(0,pd.NA) * 100
        st.markdown("### Shipping mode performance")
        st.dataframe(mode_route.style.format({"Sales":"${:,.2f}","Profit":"${:,.2f}","Profit Margin %":"{:.1f}"}), width="stretch", hide_index=True)

        order_cols = ["Order ID","Order Date","Ship Date","Ship Mode","Customer ID","City","State/Province","Region","Product Name","Units","Sales","Cost","Gross Profit"]
        order_cols = [c for c in order_cols if c in route_df.columns]
        order_details = route_df[order_cols].sort_values("Order Date", ascending=False).reset_index(drop=True)
        st.markdown("### Shipment records")
        st.dataframe(order_details, width="stretch", hide_index=True, height=430)

        csv = order_details.to_csv(index=False).encode("utf-8")
        st.download_button("Download current route records (CSV)", csv, file_name="nassau_route_records.csv", mime="text/csv")

# ============================================================
# TAB 6 — DATA QUALITY
# ============================================================
with tab_quality:
    st.markdown('<div class="section-head"><h2>Data Quality & Trust Center</h2><p>A professional analytics product should make its limitations visible instead of hiding them.</p></div>', unsafe_allow_html=True)

    missing = df.isna().sum().sum()
    duplicates = int(df.duplicated().sum())
    order_min, order_max = df["Order Date"].min(), df["Order Date"].max()
    ship_min, ship_max = df["Ship Date"].min(), df["Ship Date"].max()

    q1,q2,q3,q4 = st.columns(4)
    q1.metric("Rows", f"{len(df):,}")
    q2.metric("Columns", f"{len(df.columns):,}")
    q3.metric("Missing cells", f"{missing:,}")
    q4.metric("Exact duplicates", f"{duplicates:,}")

    st.markdown("### What is trusted in this dashboard?")
    st.success("Shipment volume, units, sales, gross profit, product, factory, destination, region and ship-mode distributions are used for descriptive analysis.")

    st.markdown("### What is deliberately not used as an operational KPI?")
    st.warning("Raw Order Date → Ship Date lead time is not presented as a verified transit-time or delay metric because the supplied dates show a systematic multi-year offset.")

    qa = pd.DataFrame({
        "Check": ["Order date range", "Ship date range", "Missing cells", "Exact duplicate rows", "Lead-time interpretation"],
        "Result": [f"{order_min:%d %b %Y} → {order_max:%d %b %Y}", f"{ship_min:%d %b %Y} → {ship_max:%d %b %Y}", f"{missing:,}", f"{duplicates:,}", "Not operationally trusted until source dates are validated"],
    })
    st.dataframe(qa, width="stretch", hide_index=True)

    st.markdown("### Recommended source correction path")
    st.markdown("1. Validate the original Order Date and Ship Date definitions with the data owner.\n2. Confirm whether Ship Date was shifted by a year offset or generated from another business calendar.\n3. Recalculate lead time only after the source correction is approved.\n4. Re-run route delay and service-level KPIs on the corrected dataset.")

# -----------------------------
# Footer
# -----------------------------
st.markdown('<div class="footer">Nassau Candy Distributor · Shipping Intelligence Command Center · Data Science Fellowship Project</div>', unsafe_allow_html=True)
