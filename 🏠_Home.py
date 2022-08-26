import requests
import streamlit as st
from streamlit_lottie import st_lottie


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_icon_01 = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5czraexr.json")
st_lottie(lottie_icon_01)

st.title("Test project - Version 1.0")
