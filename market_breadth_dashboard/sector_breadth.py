import pandas as pd
import requests
from io import StringIO
import streamlit as st

@st.cache_data(ttl=86400)
def get_sector_stocks():

    url = "https://www.niftyindices.com/IndexConstituent/ind_nifty500list.csv"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=60
    )

    df = pd.read_csv(
        StringIO(response.text)
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