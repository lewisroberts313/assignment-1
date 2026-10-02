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

st.title("26/27 Fixtures")
st.caption("Complete fixtures data for the 26/27 season")

# Fetch and cache FPL static metadata (team IDs to names)
@st.cache_data
def load_teams_mapping():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    res = requests.get(url)
    if res.status_code == 200:
        teams_data = res.json().get('teams', [])
        return {team['id']: team['name'] for team in teams_data}
    return {}

# Fetch and cache Premier League fixtures list
@st.cache_data
def get_premier_league_fixtures():
    url = "https://fantasy.premierleague.com/api/fixtures/"
    res = requests.get(url)
    if res.status_code == 200:
        return pd.DataFrame(res.json())
    return pd.DataFrame()

# Load team map and fixtures dataset
teams_map = load_teams_mapping()
fixtures_df = get_premier_league_fixtures()

if not fixtures_df.empty:
    # 1. Map Team IDs to readable names
    fixtures_df['Home Team'] = fixtures_df['team_h'].map(teams_map)
    fixtures_df['Away Team'] = fixtures_df['team_a'].map(teams_map)

    # 2. Format Kickoff Time to readable datetime string
    fixtures_df['Kickoff Time'] = pd.to_datetime(fixtures_df['kickoff_time']).dt.strftime('%b %d, %Y - %H:%M')

    # Helper function to format match score
    def format_score(row):
        if row['finished']:
            return f"{int(row['team_h_score'])} {int(row['team_a_score'])}"
        return "VS"

    # 3. Format Score column
    fixtures_df['Score'] = fixtures_df.apply(format_score, axis=1)

    # Gameweek Selector UI
    gameweeks = sorted(fixtures_df['event'].dropna().unique())
    selected_gw = st.selectbox("Select Gameweek:", gameweeks, key="gameweek_selector")

    # Filter fixtures by selected gameweek and select display columns
    gw_fixtures = fixtures_df[fixtures_df['event'] == selected_gw]
    display_df = gw_fixtures[['Kickoff Time', 'Home Team', 'Score', 'Away Team', 'finished']].rename(
        columns={'finished': 'Finished'}
    )

    # Render Fixtures Table
    st.dataframe(display_df, use_container_width=True, hide_index=True)