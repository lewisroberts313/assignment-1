import numpy as np
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="FPL expert",
    page_icon="🏆",
    layout="wide"
)

from styles import apply_styles
apply_styles()

# Load and cache FPL player data
@st.cache_data
def load_data():
    return pd.read_csv("fpl/fpl_player_statistics.csv")

df = load_data()

# Calculate points per 90 for active players (>90 mins)
df["points_per_90"] = (df["total_points"] / df["minutes"] * 90).fillna(0)
active_players = df[df["minutes"] > 90]
avg_p90 = round(active_players["points_per_90"].mean(), 2)

# Initialize session state watchlist
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# Application Title Header
st.title("FPL Expert")
st.caption("Interactive datasets and charts so you can make the right transfer for your FPL team")

tab1, tab2 = st.tabs(["Filters", "Filtered Data"])

# TAB 1: Filter Controls & Overview Metrics
with tab1:
    st.subheader("Premier League Player Statistics")

    # Initialize default filter states
    if "position_filter" not in st.session_state:
        st.session_state.position_filter = sorted(df["position_name"].dropna().unique())

    if "rating_filter" not in st.session_state:
        st.session_state.rating_filter = 0.0

    # Callback to reset filter session state
    def clear_filters():
        st.session_state.position_filter = sorted(df["position_name"].dropna().unique())
        st.session_state.total_points_filter = 0.0
        st.session_state.rating_filter = 0.0

    # Filter Inputs UI
    col1, col2 = st.columns(2)

    with col1:
        positions = st.multiselect(
            "Filter by position",
            options=sorted(df["position_name"].dropna().unique()),
            default=sorted(df["position_name"].dropna().unique()),
            key="position_filter"
        )

    with col2:
        min_rating = st.slider(
            "Total FPL points this season",
            min_value=0.0,
            max_value=float(df["total_points"].max()),
            value=0.0,
            step=0.1,
            key="total_points_filter"
        )

    st.button("Clear filters", on_click=clear_filters)

    # Filter Data based on UI input
    if min_rating == 0:
        filtered_df = df[df["position_name"].isin(positions)]
    else:
        filtered_df = df[
            (df["position_name"].isin(positions)) &
            (df["total_points"].notna()) &
            (df["total_points"] >= min_rating)
        ]
    
    # Summary Metrics Cards
    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Players shown", len(filtered_df))

    with metric2:
        st.metric("Total FPL points", round(filtered_df["total_points"].mean(), 2))

    with metric3:
        st.metric("Total goals", int(filtered_df["goals_scored"].sum()))

# TAB 2: Interactive Data Table & Analytics Charts
with tab2:
    st.subheader("Filtered Players")

    # Prepare DataFrame columns for display
    display_df = filtered_df[
        [
            "first_name",
            "second_name",
            "club_name",
            "position_name",
            "minutes",
            "goals_scored",
            "assists",
            "total_points"
        ]
    ].copy()

    # Re-evaluate Watchlist state and shift column to first position
    display_df["Watchlist"] = (
        display_df["first_name"] + " " + display_df["second_name"]
    ).isin(st.session_state.watchlist)

    watchlist_column = display_df.pop("Watchlist")
    display_df.insert(0, "Watchlist", watchlist_column)

    # Render Interactive Data Editor
    edited_df = st.data_editor(
        display_df,
        hide_index=True,
        use_container_width=True,
        disabled=[
            "first_name",
            "second_name",
            "club_name",
            "minutes",
            "goals_scored",
            "assists",
            "total_points"
        ],
        column_config={
            "Watchlist": st.column_config.CheckboxColumn(
                "Watchlist",
                help="Check to add this player to your watchlist",
                default=False
            )
        },
        key="player_watchlist"
    )

    # Vectorized extraction to append newly checked players to session state
    selected_players = (
        edited_df.loc[edited_df["Watchlist"], "first_name"] + " " + edited_df.loc[edited_df["Watchlist"], "second_name"]
    ).tolist()

    for player_name in selected_players:
        if player_name not in st.session_state.watchlist:
            st.session_state.watchlist.append(player_name)
    
    # Chart 1: Top 100 Players by Points per 90 (Min. 300 minutes played)
    st.subheader("Total FPL points per 90")

    rating_chart = (
        filtered_df[filtered_df["minutes"] >= 300]
        .sort_values(by="points_per_90", ascending=False)
        .head(100)
        .set_index("second_name")["points_per_90"]
        .round(2)
    )

    st.bar_chart(rating_chart)

    # Chart 2: Total FPL Points Aggregated by Team
    st.subheader("Total FPL points by team")
    
    team_total_points = (
        filtered_df
        .groupby("club_name")["total_points"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(team_total_points)