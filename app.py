
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="EV Charging Performance Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# BUSINESS INTELLIGENCE THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --background: #0B1220;
    --sidebar: #101827;
    --panel: #151F30;
    --border: #29364A;
    --text: #E8EEF7;
    --muted: #9AA9BD;
    --blue: #5B8DEF;
    --teal: #42B8A5;
    --amber: #E6A84A;
}

.stApp {
    background: var(--background);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding: 2rem 2.5rem 3rem;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.3px;
}

h1 {
    font-size: 2.1rem !important;
    font-weight: 700 !important;
}

p, label {
    color: var(--text);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--sidebar);
    border-right: 1px solid var(--border);
}

/* KPI cards */
[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
    transition: border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #52627A;
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: var(--blue) !important;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
}

/* Chart panels */
[data-testid="stPlotlyChart"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 8px;
}

/* Neutral business-style download button */
.stDownloadButton button {
    background: #344256 !important;
    color: #E8EEF7 !important;
    border: 1px solid #52627A !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.1rem !important;
    box-shadow: none !important;
    transition: background 0.2s ease, border-color 0.2s ease;
}

.stDownloadButton button:hover {
    background: #41516A !important;
    border-color: #71839D !important;
    color: #FFFFFF !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Inputs */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #151F30;
    border-color: #344256;
    border-radius: 8px;
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}

/* Dividers and captions */
hr {
    border-color: var(--border) !important;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

/* Status message */
[data-testid="stAlert"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA LOADING
# =========================================================
DATA_PATH = Path("data/ev_charging_cleaned.csv")


@st.cache_data
def load_data(path):
    data = pd.read_csv(path)

    # Convert datetime columns
    for column in ["StartDatetime", "EndDatetime"]:
        if column in data.columns:
            data[column] = pd.to_datetime(
                data[column],
                errors="coerce"
            )

    # Convert numeric columns safely
    numeric_columns = [
        "Duration",
        "Demand",
        "UserID",
        "ChargerID",
        "ChargerType",
        "StartHour"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    # Create date/time features if missing
    if "StartDatetime" in data.columns:
        if "StartHour" not in data.columns:
            data["StartHour"] = data["StartDatetime"].dt.hour

        if "DayOfWeek" not in data.columns:
            data["DayOfWeek"] = (
                data["StartDatetime"].dt.day_name()
            )

        if "Date" not in data.columns:
            data["Date"] = data["StartDatetime"].dt.date

    return data


if not DATA_PATH.exists():
    st.error(
        f"Dataset not found: {DATA_PATH}\n\n"
        "Please ensure ev_charging_cleaned.csv is inside "
        "the project's data folder."
    )
    st.stop()


df = load_data(DATA_PATH)

if df.empty:
    st.error("The dataset is empty. Please check your CSV file.")
    st.stop()


# =========================================================
# HEADER — NATIVE STREAMLIT COMPONENTS
# =========================================================
header_left, header_right = st.columns([5, 1])

with header_left:
    st.caption("V O L T I Q  /  E N E R G Y  I N T E L L I G E N C E")
    st.title("EV Charging Overview")
    st.write(
        "Monitor charging behavior, demand patterns, "
        "and station utilization."
    )

with header_right:
    st.write("")
    st.success("DATA LOADED")

st.divider()


# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.title("⚡Performance Analyzer")
st.sidebar.caption("EV Charging intelligence dashboard")
st.sidebar.divider()
st.sidebar.subheader("Dashboard Filters")

filtered_df = df.copy()


# ---------------------------------------------------------
# Date filter
# ---------------------------------------------------------
if "StartDatetime" in filtered_df.columns:
    valid_dates = filtered_df["StartDatetime"].dropna()

    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        selected_dates = st.sidebar.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if isinstance(selected_dates, (tuple, list)):
            if len(selected_dates) == 2:
                start_date, end_date = selected_dates

                filtered_df = filtered_df[
                    filtered_df["StartDatetime"].dt.date.between(
                        start_date,
                        end_date
                    )
                ]


# ---------------------------------------------------------
# Location filter
# ---------------------------------------------------------
if "Location" in filtered_df.columns:
    locations = sorted(
        filtered_df["Location"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_locations = st.sidebar.multiselect(
        "Charging location",
        options=locations,
        default=locations
    )

    filtered_df = filtered_df[
        filtered_df["Location"]
        .astype(str)
        .isin(selected_locations)
    ]


# ---------------------------------------------------------
# Charger company filter
# ---------------------------------------------------------
if "ChargerCompany" in filtered_df.columns:
    companies = sorted(
        filtered_df["ChargerCompany"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_companies = st.sidebar.multiselect(
        "Charger company",
        options=companies,
        default=companies
    )

    filtered_df = filtered_df[
        filtered_df["ChargerCompany"]
        .astype(str)
        .isin(selected_companies)
    ]


# ---------------------------------------------------------
# Charger type filter
# ---------------------------------------------------------
if "ChargerType" in filtered_df.columns:
    charger_types = sorted(
        filtered_df["ChargerType"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_types = st.sidebar.multiselect(
        "Charger type",
        options=charger_types,
        default=charger_types
    )

    filtered_df = filtered_df[
        filtered_df["ChargerType"].isin(selected_types)
    ]


st.sidebar.divider()
st.sidebar.caption("Invoqe Data Analytics Internship | Task 3")


# =========================================================
# KPI CARDS
# =========================================================
total_sessions = len(filtered_df)

total_users = (
    filtered_df["UserID"].nunique()
    if "UserID" in filtered_df.columns
    else 0
)

total_chargers = (
    filtered_df["ChargerID"].nunique()
    if "ChargerID" in filtered_df.columns
    else 0
)

average_duration = (
    filtered_df["Duration"].mean()
    if "Duration" in filtered_df.columns
    else float("nan")
)

average_demand = (
    filtered_df["Demand"].mean()
    if "Demand" in filtered_df.columns
    else float("nan")
)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric(
    "TOTAL CHARGING SESSIONS",
    f"{total_sessions:,}"
)

kpi2.metric(
    "ACTIVE EV USERS",
    f"{total_users:,}"
)

kpi3.metric(
    "CHARGERS UTILIZED",
    f"{total_chargers:,}"
)

kpi4.metric(
    "AVERAGE SESSION DURATION",
    f"{average_duration:.1f} min"
    if pd.notna(average_duration)
    else "N/A"
)

kpi5.metric(
    "AVERAGE CHARGING DEMAND",
    f"{average_demand:.2f}"
    if pd.notna(average_demand)
    else "N/A"
)

st.divider()


# =========================================================
# CHART 1 — CHARGING OPERATIONS TREND
# Blue = charging activity
# =========================================================
st.subheader("Charging Operations Trend")

if "StartDatetime" in filtered_df.columns:
    trend_data = filtered_df.dropna(
        subset=["StartDatetime"]
    ).copy()

    if not trend_data.empty:
        trend_data["SessionDate"] = (
            trend_data["StartDatetime"].dt.date
        )

        daily_sessions = (
            trend_data.groupby("SessionDate")
            .size()
            .reset_index(name="Sessions")
        )

        fig = px.line(
            daily_sessions,
            x="SessionDate",
            y="Sessions",
            markers=True,
            title="Daily Charging Sessions",
            template="plotly_dark"
        )

        fig.update_traces(
            line=dict(color="#5B8DEF", width=2.5),
            marker=dict(
                size=5,
                color="#5B8DEF",
                line=dict(width=1, color="#DCE7FA")
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Date",
            yaxis_title="Number of Sessions",
            margin=dict(l=20, r=20, t=55, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# CHART 2 — HOURLY UTILIZATION
# Blue = charging activity
# =========================================================
left, right = st.columns(2)


with left:
    st.subheader("Hourly Utilization")

    if "StartHour" in filtered_df.columns:
        hourly_data = (
            filtered_df.groupby("StartHour")
            .size()
            .reset_index(name="Sessions")
            .sort_values("StartHour")
        )

        fig = px.bar(
            hourly_data,
            x="StartHour",
            y="Sessions",
            title="Charging Activity by Hour",
            template="plotly_dark",
            color="Sessions",
            color_continuous_scale=[
                "#253B63",
                "#416FAF",
                "#8FB4F5"
            ]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Hour of Day",
            yaxis_title="Number of Sessions",
            coloraxis_showscale=False,
            margin=dict(l=15, r=15, t=55, b=15)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# CHART 3 — WEEKLY USAGE PATTERN
# Teal = operational usage
# =========================================================
with right:
    st.subheader("Weekly Usage Pattern")

    if "DayOfWeek" in filtered_df.columns:
        weekday_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        weekday_data = (
            filtered_df["DayOfWeek"]
            .value_counts()
            .reindex(weekday_order)
            .fillna(0)
            .rename_axis("Day")
            .reset_index(name="Sessions")
        )

        fig = px.bar(
            weekday_data,
            x="Day",
            y="Sessions",
            title="Charging Activity by Weekday",
            template="plotly_dark",
            color="Sessions",
            color_continuous_scale=[
                "#204C4A",
                "#328B80",
                "#8BD0C2"
            ]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Weekday",
            yaxis_title="Number of Sessions",
            coloraxis_showscale=False,
            margin=dict(l=15, r=15, t=55, b=15)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# CHART 4 — LOCATION PERFORMANCE
# Blue = session volume
# =========================================================
st.subheader("Location Performance")

if "Location" in filtered_df.columns:
    location_data = (
        filtered_df.groupby("Location")
        .size()
        .reset_index(name="Sessions")
        .sort_values("Sessions", ascending=False)
        .head(15)
    )

    fig = px.bar(
        location_data,
        x="Sessions",
        y="Location",
        orientation="h",
        title="Top 15 Locations by Charging Sessions",
        template="plotly_dark",
        color="Sessions",
        color_continuous_scale=[
            "#253B63",
            "#416FAF",
            "#8FB4F5"
        ]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Number of Sessions",
        yaxis_title="Location",
        coloraxis_showscale=False,
        margin=dict(l=15, r=15, t=55, b=15)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CHART 5 — DEMAND DISTRIBUTION
# Teal = demand metric
# =========================================================
left, right = st.columns(2)


with left:
    st.subheader("Charging Demand Distribution")

    if "Demand" in filtered_df.columns:
        demand_data = filtered_df.dropna(
            subset=["Demand"]
        )

        fig = px.histogram(
            demand_data,
            x="Demand",
            nbins=30,
            title="Distribution of Charging Demand",
            template="plotly_dark",
            color_discrete_sequence=["#42B8A5"]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Demand",
            yaxis_title="Number of Sessions",
            margin=dict(l=15, r=15, t=55, b=15)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# CHART 6 — SESSION DURATION
# Amber = duration metric
# =========================================================
with right:
    st.subheader("Session Duration Distribution")

    if "Duration" in filtered_df.columns:
        duration_data = filtered_df.dropna(
            subset=["Duration"]
        )

        fig = px.histogram(
            duration_data,
            x="Duration",
            nbins=30,
            title="Distribution of Session Duration",
            template="plotly_dark",
            color_discrete_sequence=["#E6A84A"]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Duration (minutes)",
            yaxis_title="Number of Sessions",
            margin=dict(l=15, r=15, t=55, b=15)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# CHART 7 — CHARGER TYPE ANALYSIS
# =========================================================
st.subheader("Charger Type Analysis")

if "ChargerType" in filtered_df.columns:
    aggregation = {
        "Sessions": ("ChargerType", "size")
    }

    if "Demand" in filtered_df.columns:
        aggregation["AverageDemand"] = ("Demand", "mean")

    if "Duration" in filtered_df.columns:
        aggregation["AverageDuration"] = ("Duration", "mean")

    charger_summary = (
        filtered_df.groupby("ChargerType")
        .agg(**aggregation)
        .reset_index()
    )

    st.dataframe(
        charger_summary,
        use_container_width=True,
        hide_index=True
    )

    if "Demand" in filtered_df.columns:
        fig = px.box(
            filtered_df.dropna(subset=["Demand"]),
            x="ChargerType",
            y="Demand",
            title="Demand Variation by Charger Type",
            template="plotly_dark",
            color="ChargerType",
            color_discrete_sequence=[
                "#5B8DEF",
                "#42B8A5",
                "#E6A84A",
                "#9B8AD8"
            ]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Charger Type",
            yaxis_title="Demand",
            showlegend=False,
            margin=dict(l=15, r=15, t=55, b=15)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# OPERATIONAL INSIGHTS
# =========================================================
st.subheader("Operational Insights")

if not filtered_df.empty:
    insight1, insight2, insight3 = st.columns(3)

    if "Location" in filtered_df.columns:
        busiest_location = filtered_df["Location"].mode()

        location_text = (
            str(busiest_location.iloc[0])
            if not busiest_location.empty
            else "N/A"
        )

        with insight1:
            st.info(
                f"**Highest Activity Location**\n\n"
                f"{location_text}"
            )

    if "StartHour" in filtered_df.columns:
        busiest_hour = filtered_df["StartHour"].mode()

        hour_text = (
            f"{int(busiest_hour.iloc[0]):02d}:00"
            if not busiest_hour.empty
            else "N/A"
        )

        with insight2:
            st.info(
                f"**Peak Charging Start Hour**\n\n"
                f"{hour_text}"
            )

    if "DayOfWeek" in filtered_df.columns:
        busiest_day = filtered_df["DayOfWeek"].mode()

        day_text = (
            str(busiest_day.iloc[0])
            if not busiest_day.empty
            else "N/A"
        )

        with insight3:
            st.info(
                f"**Highest Activity Weekday**\n\n"
                f"{day_text}"
            )

else:
    st.warning(
        "No records match the selected filters. "
        "Please adjust the filters."
    )


# =========================================================
# CHARGING TRANSACTION DETAILS
# =========================================================
st.subheader("Charging Transaction Details")

st.caption(
    "The table below reflects the current dashboard filters."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DOWNLOAD FILTERED DATA
# =========================================================
csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="ev_charging_filtered.csv",
    mime="text/csv"
)


# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "EV charging data analytics dashboard built with Streamlit and Plotly. "
    "Invoqe Data Analytics Internship — Task 3"
)