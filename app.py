
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("fifa_world_cup_2026_player_performance_dirty.csv.csv")

df = load_data()

# ---------------- TITLE ----------------
st.title("⚽ Football Analytics Dashboard")
st.markdown("### Player Performance & Tournament Analysis")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("🎯 Dashboard Filters")

team = st.sidebar.selectbox(
    "Select Team",
    ["All"] + sorted(df["team"].dropna().unique().tolist())
)

position = st.sidebar.selectbox(
    "Select Position",
    ["All"] + sorted(df["position"].dropna().unique().tolist())
)

stage = st.sidebar.selectbox(
    "Select Tournament Stage",
    ["All"] + sorted(
        df["tournament_stage"].dropna().unique().tolist()
    )
)

# ---------------- APPLY FILTERS ----------------
filtered = df.copy()

if team != "All":
    filtered = filtered[filtered["team"] == team]

if position != "All":
    filtered = filtered[filtered["position"] == position]

if stage != "All":
    filtered = filtered[filtered["tournament_stage"] == stage]

# ---------------- KPI CARDS ----------------
st.divider()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Players", len(filtered))

c2.metric(
    "Total Goals",
    int(filtered["goals"].fillna(0).sum())
)

c3.metric(
    "Average Goals",
    round(filtered["goals"].mean(), 2)
)

c4.metric(
    "Nationalities",
    filtered["nationality"].nunique()
)

st.divider()

# ---------------- CHART 1 ----------------
left, right = st.columns(2)

with left:
    st.subheader("🌍 Average Goals by Nationality")

    nationality_data = (
        filtered.groupby("nationality", as_index=False)["goals"]
        .mean()
        .sort_values("goals", ascending=False)
        .head(10)
    )

    fig1 = px.bar(
        nationality_data,
        x="nationality",
        y="goals",
        color="goals",
        text_auto=".2f",
        title="Top 10 Nationalities",
        template="plotly_dark",
        color_continuous_scale="Viridis"
    )

    fig1.update_layout(
        xaxis_title="Nationality",
        yaxis_title="Average Goals"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ---------------- CHART 2 ----------------
with right:
    st.subheader("⚽ Goals by Position")

    position_data = (
        filtered.groupby("position", as_index=False)["goals"]
        ["goals"].sum()
        .reset_index()
    )

    fig2 = px.pie(
        position_data,
        names="position",
        values="goals",
        hole=0.45,
        title="Goal Distribution by Position",
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- CHART 3 ----------------
st.subheader("🏆 Team Performance")

team_data = (
    filtered.groupby("team", as_index=False)["goals"]
    .sum()
    .sort_values("goals", ascending=False)
    .head(10)
)

fig3 = px.bar(
    team_data,
    x="team",
    y="goals",
    color="goals",
    text_auto=True,
    title="Top 10 Teams by Total Goals",
    template="plotly_dark",
    color_continuous_scale="Plasma"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.subheader("📋 Player Data")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# ---------------- DOWNLOAD DATA ----------------
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_football_data.csv",
    mime="text/csv"
)

st.success("Dashboard loaded successfully!")
