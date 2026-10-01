import streamlit as st

RED = "#DA020E"
BLACK = "#000000"
INK = "#FBE122"
PREM_GREEN = "#36FE48"
PREM_TEAL = "#04F9A5"
PREM_PURPLE = "#BF1CF0"
GREY = "#232323"
BLUE = "#4682b4"

def apply_styles():
    st.markdown( # Use markdown to apply custom CSS styles to the Streamlit app, including background color, font styles, and colors for various elements
    f"""
    <style>
        .stApp {{
            background-color: {GREY};
        }}
        h1, h2, h3 {{
            font-family: Georgia, serif !important;
            color: {BLUE} !important;
        }}
        p, li, span, .stMarkdown, .stCaption, label {{
            color: {BLUE} !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {BLUE} !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {INK} !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {BLACK};
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {INK};
        }}
    </style>
    """,
    unsafe_allow_html=True,
    )