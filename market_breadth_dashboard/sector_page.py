import pandas as pd
import streamlit as st
from datetime import datetime

from sector_breadth import get_sector_stocks
from breadth import calculate_breadth


@st.cache_data(ttl=3600)
def load_sector_breadth():

    results = []

    sector_map = get_sector_stocks()

    for sector, stocks in sector_map.items():

        try:

            symbols = [
                stock["symbol"]
                for stock in stocks
            ]

            result = calculate_breadth(symbols)

            if result:

                results.append({
                    "Sector": sector,
                    "Stocks": len(symbols),
                    "EMA20": result["EMA20"],
                    "EMA50": result["EMA50"],
                    "EMA100": result["EMA100"],
                    "EMA200": result["EMA200"]
                })

        except Exception:
            continue

    return pd.DataFrame(results)


def show_sector_page():

    st.subheader("🏭 Sector Breadth")

    st.caption(
        "Using complete sector constituents (full universe)"
    )

    with st.spinner("Loading sector breadth..."):

        df = load_sector_breadth()

    st.caption(
        f"Last Updated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"
    )

    if df.empty:

        st.error("No sector data available")
        return

    # Sort by EMA20 strongest first
    df = df.sort_values(
        "EMA20",
        ascending=False
    ).reset_index(drop=True)

    top5 = df.nlargest(
        5,
        "EMA20"
    ).reset_index(drop=True)

    bottom5 = (
        df.nsmallest(
            5,
            "EMA20"
        )
        .sort_values(
            "EMA20"
        )
        .reset_index(drop=True)
    )

    top5_display = top5[
        ["Sector", "EMA20"]
    ].copy()

    bottom5_display = bottom5[
        ["Sector", "EMA20"]
    ].copy()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏆 Strongest Sectors")

        strongest_styled = (
            top5_display.style
            .background_gradient(
                cmap="RdYlGn",
                subset=["EMA20"],
                vmin=0,
                vmax=100
            )
            .format({
                "EMA20": "{:.0f}%"
            })
        )

        st.table(strongest_styled)

    with col2:

        st.subheader("❌ Weakest Sectors")

        weakest_styled = (
            bottom5_display.style
            .background_gradient(
                cmap="RdYlGn",
                subset=["EMA20"],
                vmin=0,
                vmax=100
            )
            .format({
                "EMA20": "{:.0f}%"
            })
        )

        st.table(weakest_styled)

    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Sector Breadth CSV",
        csv,
        "sector_breadth.csv",
        "text/csv"
    )

    heatmap_df = df.copy()

    styled_df = (
        heatmap_df.style
        .background_gradient(
            cmap="RdYlGn",
            subset=[
                "EMA20",
                "EMA50",
                "EMA100",
                "EMA200"
            ],
            vmin=0,
            vmax=100
        )
        .format({
            "EMA20": "{:.0f}%",
            "EMA50": "{:.0f}%",
            "EMA100": "{:.0f}%",
            "EMA200": "{:.0f}%"
        })
    )

    st.subheader("📊 Sector Heatmap")

    st.table(styled_df)

    st.caption(
        f"Sectors Analysed: {len(df)}"
    )