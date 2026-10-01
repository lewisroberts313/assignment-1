import streamlit as st  # Import the Streamlit library for building interactive web applications
import pandas as pd  # Import the Pandas library for data manipulation and analysis
import numpy as np  # Import the NumPy library for numerical computing

from PIL import Image  # Import Image module from PIL library to open and manipulate images
from styles import apply_styles  # Import apply_styles function from the styles module

apply_styles()  # Apply custom CSS styles to the Streamlit app

# Load the CSV  and cache it so it is only read once per session.
@st.cache_data  # Decorate function to cache dataset loading in memory
def load_data():  # Define function to read player data from CSV file
    # Read the CSV file into a DataFrame.
    data = pd.read_csv("fpl/fpl_player_statistics.csv") # load the dataset
    # Return the DataFrame to the caller.
    return data  # Return loaded DataFrame to caller

df = load_data() # Call the cached loader to get the survey data




st.set_page_config(page_title="FPL expert", page_icon="\U0001F3C6", layout="wide") # Set the page configuration for the Streamlit app, including the title, icon, and layout

st.title("About") # Set the title of the Streamlit app

col1, col2 = st.columns(2) # Create two columns for layout

with col1:  # Enter context for first column
    st.header("Problem Statement") # Add a header for the problem statement section
    st.write("As an FPL player, I find that the official FPL website provides a lot of statistics, but it can be difficult to quickly compare players and find the information I am looking for. This app is designed to make that process easier by allowing FPL players to filter, compare, and visualize player statistics in one place. This helps users explore player performance without having to search through large amounts of data.")  # Render problem statement explanatory text
with col2:  # Enter context for second column
    image = Image.open("fpl_interface.png") # Open the image file for the FPL interface
    st.image(image, caption="*screenshot of the FPL interface when displaying player statistics*", width=400, use_container_width=False)  # Display image widget with specified caption, width, and container scaling parameters