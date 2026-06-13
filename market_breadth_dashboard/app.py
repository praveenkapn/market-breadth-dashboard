import streamlit as st
import pandas as pd

from sector_page import show_sector_page
from data_fetcher import get_index_constituents
from breadth import calculate_breadth
from sector_inspector import show_sector_inspector


st.set_page_config(
    page_title="Market Breadth Dashboard",
    layout="wide"
)

st.title("📈 Market Breadth Dashboard")

page = st.sidebar.selectbox(
    "Select Page",
    [
        "Index Breadth",
        "Sector Breadth",
        "Sector Inspector"
    ]
)

if st.sidebar.button("🔄 Refresh All Data"):
    st.cache_data.clear()
    st.rerun()

if page == "Index Breadth":

    indices = [
        "Nifty 50",
        "Nifty 500",
        "Nifty Midcap 150",
        "Nifty Smallcap 250"
    ]

    results = []

    for idx in indices:

        with st.spinner(f"Processing {idx}..."):

            stocks = get_index_constituents(idx)

            result = calculate_breadth(stocks)

            if result:

                results.append({
                    "Index": idx,
                    "EMA20": result["EMA20"],
                    "EMA50": result["EMA50"],
                    "EMA100": result["EMA100"],
                    "EMA200": result["EMA200"]
                })

    df = pd.DataFrame(results)

    styled_df = (
        df.style
        .background_gradient(
            cmap="RdYlGn",
            subset=[
                "EMA20",
                "EMA50",
                "EMA100",
                "EMA200"
            ]
        )
        .format({
            "EMA20": "{:.0f}%",
            "EMA50": "{:.0f}%",
            "EMA100": "{:.0f}%",
            "EMA200": "{:.0f}%"
        })
    )

    st.subheader("📊 Index Breadth Heatmap")

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Index Breadth CSV",
        csv,
        "index_breadth.csv",
        "text/csv"
    )

elif page == "Sector Breadth":

    show_sector_page()

elif page == "Sector Inspector":

    show_sector_inspector()