import pandas as pd
import streamlit as st

# Configure page settings
st.set_page_config(page_title="Player Search", layout="wide")

from styles import apply_styles
apply_styles()

st.title("Player Search")

# Load and cache FPL player data
@st.cache_data
def load_data():
    return pd.read_csv("fpl/fpl_player_statistics.csv")

df = load_data()

# Search Query Input UI
search_query = st.text_input(
    "Search for a player by name:",
    placeholder="e.g. Haaland, Salah, Saka..."
)

# Filter and Display Matching Player Stats
if search_query.strip():
    # Case-insensitive search on player surname
    filtered_df = df[df["second_name"].str.contains(search_query, case=False, na=False)]
    
    if not filtered_df.empty:
        st.write(f"Found {len(filtered_df)} matching player(s):")
        
        # Display expandable detailed view for each matched player
        for player_row in filtered_df.itertuples():
            first_name = getattr(player_row, 'first_name', 'First Name')
            second_name = getattr(player_row, 'second_name', 'Second Name')
            
            with st.expander(f"📊 Detailed View: {first_name} {second_name}", expanded=False):
                # Convert row Series into a clean key-value stat table
                player_stats = df.loc[player_row.Index].to_frame().reset_index()
                player_stats.columns = ["Metric / Stat", "Value"]
                st.table(player_stats)
    else:
        st.warning("No players found matching that name.")
else:
    st.info("Type a player's name above to view their statistics.")