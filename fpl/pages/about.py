import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

# Configure page settings (must be the first Streamlit command)
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

# Page Title & Header
st.title("About")

# Layout: Problem Statement & Interface Screenshot
col1, col2 = st.columns(2)

with col1:
    st.header("Problem Statement")
    st.write(
        "As an FPL player, I find that the official FPL website provides a lot of statistics, "
        "but it can be difficult to quickly compare players and find the information I am looking for. "
        "This app is designed to make that process easier by allowing FPL players to filter, compare, "
        "and visualize player statistics in one place. This helps users explore player performance "
        "without having to search through large amounts of data."
    )

with col2:
    image = Image.open("fpl/fpl_interface.png")
    st.image(
        image,
        caption="*screenshot of the FPL interface when displaying player statistics*",
        width=400,
        use_container_width=False
    )