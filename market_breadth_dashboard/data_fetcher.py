import pandas as pd
import requests
from io import StringIO

import streamlit as st

INDEX_URLS = {
    "Nifty 50": "https://www.niftyindices.com/IndexConstituent/ind_nifty50list.csv",
    "Nifty 500": "https://www.niftyindices.com/IndexConstituent/ind_nifty500list.csv",
    "Nifty Midcap 150": "https://www.niftyindices.com/IndexConstituent/ind_niftymidcap150list.csv",
    "Nifty Smallcap 250": "https://www.niftyindices.com/IndexConstituent/ind_niftysmallcap250list.csv"
}
@st.cache_data(ttl=86400)
def get_index_constituents(index_name):

    url = INDEX_URLS[index_name]

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        ),
        "Accept": "text/csv,text/plain,*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.niftyindices.com/",
        "Origin": "https://www.niftyindices.com"
    }

    session = requests.Session()

    response = session.get(
        url,
        headers=headers,
        timeout=60
    )

    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text)
    )

    symbols = df["Symbol"].dropna().tolist()

    return [f"{symbol}.NS" for symbol in symbols]
