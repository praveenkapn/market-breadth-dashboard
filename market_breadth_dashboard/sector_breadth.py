import pandas as pd
import streamlit as st


@st.cache_data(ttl=86400)
def get_sector_stocks():

    df = pd.read_csv(
        "data/nifty500.csv"
    )

    sector_map = {}

    for _, row in df.iterrows():

        sector = row["Industry"]
        symbol = row["Symbol"]
        company = row["Company Name"]

        if str(symbol).startswith("DUMMY"):
            continue

        symbol = symbol + ".NS"

        if sector not in sector_map:
            sector_map[sector] = []

        sector_map[sector].append({
            "symbol": symbol,
            "company": company
        })

    return sector_map
