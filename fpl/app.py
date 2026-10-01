import streamlit as st  # Import the Streamlit library for building interactive web applications
import pandas as pd  # Import the Pandas library for data manipulation and analysis
import numpy as np  # Import the NumPy library for numerical computing
import requests  # Import the Requests library for making HTTP requests

st.set_page_config(  # Set the page configuration for the Streamlit app
    page_title="FPL expert",  # Set the title of the browser tab
    page_icon="\U0001F3C6",  # Set the tab icon using a unicode emoji
    layout="wide"  # Set the layout mode to wide
)  # Close page configuration call


from styles import apply_styles  # Import apply_styles function from the styles module
apply_styles()  # Apply the custom styles to the app

# Load the CSV  and cache it so it is only read once per session.
@st.cache_data  # Decorate function to cache the loaded data in memory
def load_data():  # Define function to load player data from CSV file
    # Read the CSV file into a DataFrame.
    data = pd.read_csv("fpl_player_statistics.csv")  # Read CSV into a pandas DataFrame
    # Return the DataFrame to the caller.
    return data  # Return the DataFrame

df = load_data()  # Load data into df variable via cached function call

df["points_per_90"] = (df["total_points"] / df["minutes"] * 90).fillna(0)  # Compute points per 90 minutes and fill NaN values with 0

active_players = df[df["minutes"] > 90]  # Filter dataframe to include only players with over 90 minutes played
avg_p90 = round(active_players["points_per_90"].mean(), 2)  # Calculate mean points per 90 for active players, rounded to 2 decimals

# Create the watchlist if it does not already exist
if "watchlist" not in st.session_state:  # Check if watchlist key exists in session state
    st.session_state.watchlist = []  # Initialize watchlist as an empty list in session state

st.title("FPL Expert")  # Render main title header on the page
st.caption("Interactive datasets and charts so you can make the right transfer for your FPL team")  # Display subtitle caption below the title

tab1, tab2 = st.tabs(["Filters", "Filtered Data"])  # Create two navigation tabs

with tab1:  # Enter tab1 context for main filter controls
    st.subheader("Premier League Player Statistics")  # Add a section subheader inside tab1

    if "position_filter" not in st.session_state:  # Check if position filter state exists
        st.session_state.position_filter = sorted(  # Set position filter default list in session state
            df["position_name"].dropna().unique()  # Extract sorted unique non-null position names
        )  # Complete position filter list initialization

    if "rating_filter" not in st.session_state:  # Check if rating filter state exists
        st.session_state.rating_filter = 0.0  # Initialize default rating filter to 0.0 in session state

    def clear_filters():  # Define callback function to reset all session filter values
        st.session_state.position_filter = sorted(  # Reset position filter list in session state
            df["position_name"].dropna().unique()  # Extract sorted unique position names
        )  # Complete position filter reset
        st.session_state.total_points_filter = 0.0  # Reset total points slider state to 0.0
        st.session_state.rating_filter = 0.0  # Reset rating filter state to 0.0

    # FILTERS
    col1, col2 = st.columns(2)  # Split layout into 2 side-by-side columns

    with col1:  # Enter first column context
        positions = st.multiselect(  # Display multiselect widget for positions
            "Filter by position",  # Set multiselect input field label
            options=sorted(df["position_name"].dropna().unique()),  # Provide all sorted unique positions as options
            default=sorted(df["position_name"].dropna().unique()),  # Set all positions as default selection
            key="position_filter"  # Bind selection state to session state key
        )  # Complete multiselect configuration

    with col2:  # Enter second column context
        min_rating = st.slider(  # Display slider widget for filtering points
            "Total FPL points this season",  # Set slider input label
            min_value=0.0,  # Set lower bound for slider
            max_value=float(df["total_points"].max()),  # Set upper bound to max total points in dataset
            value=0.0,  # Set initial default value for slider
            step=0.1,  # Set increment step size for slider
            key="total_points_filter"  # Bind slider value to session state key
        )  # Complete slider configuration

    # CLEAR FILTERS BUTTON
    st.button(  # Display action button to clear all current filters
        "Clear filters",  # Set button label text
        on_click=clear_filters  # Attach clear_filters callback on button press
    )  # Complete button configuration

    # APPLY FILTERS
    if min_rating == 0:  # Check if slider filter is set to 0
        filtered_df = df[  # Filter dataset by selected positions only
            df["position_name"].isin(positions)  # Filter condition checking position match
        ]  # Finalize position-only filtering
    else:  # Handle case when slider value is greater than 0
        filtered_df = df[  # Filter dataset by position and points criteria
            (df["position_name"].isin(positions)) &  # Check position matches selected list
            (df["total_points"].notna()) &  # Check total points value is present
            (df["total_points"] >= min_rating)  # Check total points meets or exceeds minimum rating threshold
        ]  # Finalize combined filtering
    
    # METRICS
    metric1, metric2, metric3 = st.columns(3)  # Divide layout into 3 columns for metric cards

    with metric1:  # Enter metric column 1
        st.metric(  # Display metric card
            "Players shown",  # Set metric card title label
            len(filtered_df)  # Show count of currently filtered rows
        )  # Complete first metric display

    with metric2:  # Enter metric column 2
        st.metric(  # Display metric card
            "Total FPL points",  # Set metric card title label
            round(filtered_df["total_points"].mean(), 2)  # Calculate and display average total points rounded to 2 decimal places
        )  # Complete second metric display

    with metric3:  # Enter metric column 3
        st.metric(  # Display metric card
            "Total goals",  # Set metric card title label
            int(filtered_df["goals_scored"].sum())  # Sum total goals scored in filtered dataset converted to integer
        )  # Complete third metric display


with tab2:  # Enter tab2 context for displaying data and charts

    # TABLE
    st.subheader("Filtered Players")  # Add section subheader for data table

    # Create the table to display
    display_df = filtered_df[  # Select specific columns to display in table
        [  # Begin column list definition
            "first_name",  # Select first name column
            "second_name",  # Select second name column
            "club_name",  # Select club name column
            "position_name",  # Select position column
            "minutes",  # Select minutes played column
            "goals_scored",  # Select goals scored column
            "assists",  # Select assists column
            "total_points"  # Select total points column
        ]  # End column list definition
    ].copy()  # Create a deep copy of selected columns dataframe


    # Set the Watchlist checkbox based on the current watchlist
    display_df["Watchlist"] = (  # Add dynamic boolean Watchlist column
        display_df["first_name"] + " " + display_df["second_name"]  # Concatenate player full name
    ).isin(st.session_state.watchlist)  # Check if player full name exists in session state watchlist


    # Put Watchlist at the beginning
    watchlist_column = display_df.pop("Watchlist")  # Extract Watchlist column from original position
    display_df.insert(0, "Watchlist", watchlist_column)  # Insert Watchlist column at the first index position


    # Display the table
    edited_df = st.data_editor(  # Render interactive data editor widget
        display_df,  # Pass dataframe to display editor
        hide_index=True,  # Hide dataframe index column
        use_container_width=True,  # Expand editor to full width of container
        disabled=[  # List columns that cannot be directly edited by user
            "first_name",  # Disable editing for first_name
            "second_name",  # Disable editing for second_name
            "club_name",  # Disable editing for club_name
            "minutes",  # Disable editing for minutes
            "goals_scored",  # Disable editing for goals_scored
            "assists",  # Disable editing for assists
            "total_points"  # Disable editing for total_points
        ],  # End disabled columns list
        column_config={  # Configure specific column display formats
            "Watchlist": st.column_config.CheckboxColumn(  # Configure Watchlist as checkbox column type
                "Watchlist",  # Set header text for column
                help="Check to add this player to your watchlist",  # Set hover tooltip help text
                default=False  # Set default checkbox state to unchecked
            )  # Complete checkbox configuration
        },  # Complete column configurations dictionary
        key="player_watchlist"  # Assign key name for data editor widget state
    )  # Finalize data editor display setup

    # Update the watchlist based on the checkboxes
    for _, row in edited_df.iterrows():  # Iterate through rows of user-edited table

        player_name = f"{row['first_name']} {row['second_name']}"  # Construct full player name string

        if row["Watchlist"]:  # Check if user selected Watchlist checkbox for this player
            if player_name not in st.session_state.watchlist:  # Check if player is not already present in watchlist list
                st.session_state.watchlist.append(player_name)  # Add new player name to watchlist list in session state

    
    # CHART 1
    st.subheader("Total FPL points per 90")  # Add chart section header

    rating_chart = (  # Build series for points per 90 bar chart
        filtered_df[filtered_df["minutes"] >= 300]  # Filter players with at least 300 minutes played
        .sort_values(by="points_per_90", ascending=False)  # Sort filtered dataset by points per 90 in descending order
        .head(100)  # Take top 100 players from sorted dataset
        .set_index("second_name")["points_per_90"]  # Set index to player last name and extract points_per_90 column
        .round(2)  # Round values in series to 2 decimal places
    )  # Complete chart dataset transformation pipeline

    st.bar_chart(rating_chart)  # Render Streamlit bar chart for top players by points per 90

    st.subheader("Total FPL points by team")  # Add team aggregated chart subheader
    team_total_points = (  # Build aggregated series for team total points chart
    filtered_df  # Take current filtered dataframe
    .groupby("club_name")["total_points"]  # Group data by club name and select total points
    .sum()  # Calculate total points sum per club
    .sort_values(ascending=False)  # Sort total team points descending
    )  # Complete aggregation pipeline

    st.bar_chart(team_total_points)  # Render Streamlit bar chart for total points grouped by team