import pandas as pd
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="FPL Watchlist",
    layout="wide"
)

from styles import apply_styles
apply_styles()

# Load and cache FPL player data
@st.cache_data
def load_data():
    return pd.read_csv("fpl/fpl_player_statistics.csv")

df = load_data()

st.title("FPL Watchlist")

# Initialize session state watchlist if needed
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# Display info notice if watchlist is empty
if len(st.session_state.watchlist) == 0:
    st.info(
        "Your watchlist is empty. "
        "Go to the player statistics page and tick players to add them."
    )

else:
    # Filter dataset for saved watchlist players
    watchlist_df = df[
        (df["first_name"] + " " + df["second_name"]).isin(st.session_state.watchlist)
    ].copy()

    st.subheader(f"Players on your watchlist: {len(watchlist_df)}")

    # Select columns to display
    display_columns = [
        "first_name",
        "second_name",
        "club_name",
        "position_name",
        "minutes",
        "goals_scored",
        "assists",
        "total_points"
    ]

    display_df = watchlist_df[display_columns].copy()

    # Add interactive Remove checkbox column at position 0
    display_df.insert(0, "Remove", False)

    # Render interactive data editor
    edited_df = st.data_editor(
        display_df,
        hide_index=True,
        use_container_width=True,
        disabled=display_columns,
        column_config={
            "Remove": st.column_config.CheckboxColumn(
                "Remove",
                help="Tick this box to remove the player from your watchlist",
                default=False
            )
        },
        key="watchlist_editor"
    )

    # Extract names of players marked for removal via vectorized selection
    players_to_remove = (
        edited_df.loc[edited_df["Remove"], "first_name"] + " " + edited_df.loc[edited_df["Remove"], "second_name"]
    ).tolist()

    # Remove selected players from session state and refresh page
    if players_to_remove:
        st.session_state.watchlist = [
            player for player in st.session_state.watchlist if player not in players_to_remove
        ]
        st.rerun()