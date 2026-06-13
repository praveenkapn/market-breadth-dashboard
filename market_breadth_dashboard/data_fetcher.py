import pandas as pd
import streamlit as st

LOCAL_FILES = {
    "Nifty 50": "data/nifty50.csv",
    "Nifty 500": "data/nifty500.csv",
    "Nifty Midcap 150": "data/midcap150.csv",
    "Nifty Smallcap 250": "data/smallcap250.csv"
}


@st.cache_data(ttl=86400)
def get_index_constituents(index_name):

    df = pd.read_csv(
        LOCAL_FILES[index_name]
    )

    symbols = (
        df["Symbol"]
        .dropna()
        .tolist()
    )

    return [
        f"{symbol}.NS"
        for symbol in symbols
    ]
