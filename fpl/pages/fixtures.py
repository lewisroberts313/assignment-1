import streamlit as st  # Import the Streamlit library for building interactive web applications
import pandas as pd  # Import the Pandas library for data manipulation and analysis
import numpy as np  # Import the NumPy library for numerical computing
import requests  # Import the Requests library for making HTTP requests

st.set_page_config(  # Set the page configuration for the Streamlit app
    page_title="FPL expert",  # Set the title of the browser tab
    page_icon="\U0001F3C6",  # Set the tab icon using a unicode emoji
    layout="wide"  # Set the layout mode to wide
) # Set the page configuration for the Streamlit app, including the title, icon, and layout

from styles import apply_styles  # Import apply_styles function from the styles module
apply_styles()  # Apply custom CSS styles to the Streamlit app

st.title("26/27 Fixtures") # Set the title of the Streamlit app
st.caption("Complete fixtures data for the 26/27 season") # Add a caption below the title to describe the dashboard as containing real, verified football data and built with various Streamlit components

@st.cache_data  # Decorate function to cache loaded team mapping data in memory
def load_teams_mapping():  # Define function to fetch and map team IDs to names
    # Public endpoint containing general metadata including team names
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"  # Define API URL for general FPL static metadata
    res = requests.get(url)  # Send HTTP GET request to the static endpoint
    if res.status_code == 200:  # Check if the API request was successful
        teams_data = res.json().get('teams', [])  # Extract teams array from response JSON or default to empty list
        # Create a dictionary mapping team ID -> Team Name
        return {team['id']: team['name'] for team in teams_data}  # Return dictionary mapping team ID to team name
    return {}  # Return empty dictionary if request failed

@st.cache_data  # Decorate function to cache premier league fixtures data in memory
def get_premier_league_fixtures():  # Define function to fetch fixture data from API
    url = "https://fantasy.premierleague.com/api/fixtures/"  # Define API URL for FPL fixtures data
    res = requests.get(url)  # Send HTTP GET request to the fixtures endpoint
    if res.status_code == 200:  # Check if the API request was successful
        return pd.DataFrame(res.json())  # Convert JSON response into a pandas DataFrame and return it
    return pd.DataFrame()  # Return empty DataFrame if request failed

# Load mapping dictionary and fixtures
teams_map = load_teams_mapping()  # Fetch team ID to name mapping dictionary
fixtures_df = get_premier_league_fixtures()  # Fetch Premier League fixtures DataFrame

if not fixtures_df.empty:  # Check if fixtures DataFrame is not empty
    # 1. Map Team IDs to Team Names
    fixtures_df['Home Team'] = fixtures_df['team_h'].map(teams_map)  # Map home team IDs to team names
    fixtures_df['Away Team'] = fixtures_df['team_a'].map(teams_map)  # Map away team IDs to team names

    # 2. Format Kickoff Time to readable datetime
    fixtures_df['Kickoff Time'] = pd.to_datetime(fixtures_df['kickoff_time']).dt.strftime('%b %d, %Y - %H:%M')  # Convert ISO kickoff time to formatted datetime string

    # 3. Format Scores (show 'VS' if match hasn't been played yet)
    fixtures_df['Score'] = fixtures_df.apply(  # Create formatted Score string column based on match state
        lambda r: f"{int(r['team_h_score'])} {int(r['team_a_score'])}" if r['finished'] else "VS",  # Return formatted score string if finished, else return VS string
        axis=1  # Apply score calculation logic across each row
    )  # Complete Score column creation

    # Gameweek Selector
    gameweeks = sorted(fixtures_df['event'].dropna().unique())  # Get sorted unique non-null gameweek numbers
    selected_gw = st.selectbox("Select Gameweek:", gameweeks, key="gameweek_selector")  # Render selectbox dropdown widget for picking gameweek

    # Filter by selected Gameweek and select clean columns
    gw_fixtures = fixtures_df[fixtures_df['event'] == selected_gw]  # Filter fixtures DataFrame by selected gameweek
    display_df = gw_fixtures[['Kickoff Time', 'Home Team', 'Score', 'Away Team', 'finished']].rename(  # Select display columns and rename finished column
        columns={'finished': 'Finished'}  # Rename finished column to Finished for clean display
    )  # Complete display DataFrame preparation

    # Display clean table
    st.dataframe(display_df, use_container_width=True, hide_index=True)  # Render formatted fixtures DataFrame table in Streamlit