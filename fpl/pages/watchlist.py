import streamlit as st  # Import the Streamlit library for building interactive web applications
import pandas as pd  # Import the Pandas library for data manipulation and analysis

st.set_page_config(  # Set the page configuration for the Streamlit app
    page_title="FPL Watchlist",  # Set the title of the browser tab
    layout="wide"  # Set the layout mode of the Streamlit app to wide
)  # Complete page configuration call

from styles import apply_styles  # Import the apply_styles function from the styles module
apply_styles()  # Execute the custom CSS styling rules for the application


# Load the data
@st.cache_data  # Decorate function to cache loaded data in memory for better performance
def load_data():  # Define cached function to load the dataset
    return pd.read_csv("fpl/fpl_player_statistics.csv")  # Read player statistics CSV and return as DataFrame


df = load_data()  # Load the dataset into the df variable via cached function call


st.title("FPL Watchlist")  # Render main title header for the Watchlist page


# Make sure watchlist exists
if "watchlist" not in st.session_state:  # Check if watchlist key exists in session state
    st.session_state.watchlist = []  # Initialize watchlist as an empty list in session state


# Check if watchlist is empty
if len(st.session_state.watchlist) == 0:  # Check if the watchlist list contains zero players

    st.info(  # Display informational banner message
        "Your watchlist is empty. "  # Message sentence 1 explaining empty state
        "Go to the player statistics page and tick players to add them."  # Message sentence 2 detailing instructions
    )  # Complete info banner display

else:  # Handle case when watchlist contains one or more players

    # Get players currently in the watchlist
    watchlist_df = df[  # Filter main DataFrame for players present in watchlist
        (df["first_name"] + " " + df["second_name"]).isin(  # Concatenate full name and match against watchlist
            st.session_state.watchlist  # Reference session state watchlist list
        )  # Complete condition check
    ].copy()  # Create an explicit copy of the filtered DataFrame

    st.subheader(  # Render subheader displaying count of saved players
        f"Players on your watchlist: {len(watchlist_df)}"  # Format dynamic string showing total watchlist count
    )  # Complete subheader display


    # Columns to display
    display_columns = [  # Define list of relevant column names for the table view
        "first_name",  # Player first name column
        "second_name",  # Player second name column
        "club_name",  # Player club name column
        "position_name",  # Player position name column
        "minutes",  # Total minutes played column
        "goals_scored",  # Total goals scored column
        "assists",  # Total assists column
        "total_points"  # Total FPL points column
    ]  # Complete column selection array


    # Create a copy of the data for the table
    display_df = watchlist_df[display_columns].copy()  # Filter display columns and create a deep copy


    # Add a Remove checkbox at the beginning of the table
    display_df.insert(0, "Remove", False)  # Insert Remove boolean column populated with False at index 0


    # Display the editable table
    edited_df = st.data_editor(  # Render interactive data editor widget
        display_df,  # Pass display DataFrame to data editor
        hide_index=True,  # Hide DataFrame index column in table output
        use_container_width=True,  # Expand table width to match container width
        disabled=display_columns,  # Disable editing on data columns to make them read-only
        column_config={  # Provide custom widget config for specific columns
            "Remove": st.column_config.CheckboxColumn(  # Configure Remove column as interactive checkbox
                "Remove",  # Set column header display label
                help="Tick this box to remove the player from your watchlist",  # Set hover tooltip explanation
                default=False  # Set default checkbox value to unchecked
            )  # Complete CheckboxColumn configuration
        },  # Complete column_config dictionary
        key="watchlist_editor"  # Assign unique widget key for tracking session state
    )  # Complete data_editor call


    # Find players that have been selected for removal
    players_to_remove = []  # Initialize empty list to accumulate player names marked for removal

    for _, row in edited_df.iterrows():  # Iterate through every row in user-edited table

        if row["Remove"]:  # Check if the Remove checkbox is checked for the current row

            player_name = (  # Construct player full name string
                f"{row['first_name']} {row['second_name']}"  # Combine first and second name with space
            )  # Complete string formatting

            players_to_remove.append(player_name)  # Append player name to removal list


    # Remove selected players
    if players_to_remove:  # Check if there are any players marked for removal

        for player_name in players_to_remove:  # Loop over names in removal list

            if player_name in st.session_state.watchlist:  # Verify player exists in session state watchlist
                st.session_state.watchlist.remove(player_name)  # Remove player name from session state list

        st.rerun()  # Trigger app rerun to instantly reflect updated watchlist UI