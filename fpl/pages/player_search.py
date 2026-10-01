import streamlit as st  # Import the Streamlit library for building interactive web applications
import pandas as pd  # Import the Pandas library for data manipulation and analysis

st.set_page_config(page_title="Player Search", layout="wide")  # Set page configuration with title and wide layout

from styles import apply_styles  # Import apply_styles function from styles module
apply_styles()  # Apply custom CSS styles to the Streamlit app

st.title("Player Search")  # Render page title header with emoji

# 1. Load data
@st.cache_data  # Decorate function to cache dataset loading in memory
def load_data():  # Define function to read player data from CSV file
    # Adjust path if your CSV file is located elsewhere
    df = pd.read_csv("fpl_player_statistics.csv")  # Read CSV file into a pandas DataFrame
    return df  # Return loaded DataFrame to caller

df = load_data()  # Load data into df variable via cached loader function

# 2. Single text input for searching player names
search_query = st.text_input("Search for a player by name:", placeholder="e.g. Haaland, Salah, Saka...")  # Render search text input widget with placeholder text

# 3. Filter and display player stats
if search_query.strip():  # Check if user search query contains non-whitespace text
    # Filter dataset (case-insensitive search)
    filtered_df = df[df["second_name"].str.contains(search_query, case=False, na=False)]  # Filter DataFrame by matching query against second_name column
    
    if not filtered_df.empty:  # Check if filtered search results DataFrame is not empty
        st.write(f"Found {len(filtered_df)} matching player(s):")  # Display count of matching players found
        
        for _, player_row in filtered_df.iterrows():  # Loop through each matching player row in filtered DataFrame
            with st.expander(f"📊 Detailed View: {player_row.get('first_name', 'First Name')} {player_row.get('second_name', 'Second Name')}", expanded=False):  # Create expandable container labeled with player name
                player_stats = player_row.to_frame().reset_index()  # Convert player series into two-column DataFrame and reset index
                player_stats.columns = ["Metric / Stat", "Value"]  # Rename DataFrame columns for clear table presentation
                st.table(player_stats)  # Render static table showing all player metrics and values
    else:  # Handle case when search query yields no matching rows
        st.warning("No players found matching that name.")  # Display warning banner message for no matches
else:  # Handle case when search query input field is empty
    st.info("Type a player's name above to view their statistics.")  # Display informational guidance banner to user