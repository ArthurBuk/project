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

st.title("Hello, this app provides analysis of the following ETFs:\n"
         "## 1) S&P500\n"
         "## 2) DOW\n"
         "## 3) NASDAQ\n")





