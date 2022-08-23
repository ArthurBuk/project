import streamlit as st
from streamlit_option_menu import option_menu

# create a sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["About", "Stock Data"]
    )

if selected == "About":
    st.title("""
    Choose a page in the Navigation section
    """)

if selected == "Stock Data":
    st.title(f"{selected} page")

