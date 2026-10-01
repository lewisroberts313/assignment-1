Introduction & Overview

Brief intro: FPL Expert dashboard built using Streamlit, Python, and Pandas.

Key goal: Simplify player statistical analysis and transfer planning for FPL managers.

Technical Architecture & Data Pipeline

Cached data loading (@st.cache_data) for high performance and reduced server load.

Dynamic filtering via st.session_state allowing cross-tab persistence (filters, watchlists).

Direct integration with the official Premier League API for real-time fixture and team mapping.

Key UI/UX Features

Interactive Player Metrics: Custom slider/multiselect filters with aggregated team metrics.

Watchlist Manager: Dynamic dataframe editor (st.data_editor) with quick add/remove checkboxes.

Player Search: Instant case-insensitive search displaying full stat breakdowns in collapsible expanders.

Custom Styling: Injected CSS via styles.py to maintain a sleek, dark-themed Premier League look.

Demonstration Steps

Showcase filtering by position and min points on the statistics page.

Add key players to the Watchlist and view them on the Watchlist tab.

Demonstrate fixture lookup for upcoming gameweeks.

Conclude with a quick player name search.