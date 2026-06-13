import streamlit as st
from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder

from sector_breadth import get_sector_stocks
from breadth import get_stock_details


def show_sector_inspector():

    st.subheader("🔍 Sector Inspector")

    sector_map = get_sector_stocks()

    sector = st.selectbox(
        "Select Sector",
        sorted(sector_map.keys())
    )

    stocks = sector_map[sector]

    symbols = [
        stock["symbol"]
        for stock in stocks
    ]

    st.caption(
        f"Total Stocks in Sector: {len(symbols)}"
    )

    with st.spinner(
        "Calculating stock level EMA data..."
    ):

        df = get_stock_details(
            symbols,
            stocks
        )

    if df.empty:

        st.error("No data found")
        return

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(
        sortable=True,
        filter=True,
        resizable=True
    )

    gb.configure_grid_options(
        enableRangeSelection=True,
        enableCellTextSelection=True,
        rowHeight=32
    )

    # Wider company name column
    gb.configure_column(
        "Company Name",
        width=300
    )

    gb.configure_column(
        "Stock Symbol",
        width=120
    )

    custom_css = {
        ".ag-header": {
            "background-color": "#f8fafc !important"
        },
        ".ag-header-cell-label": {
            "color": "#111827 !important",
            "font-weight": "700 !important",
            "font-size": "15px !important"
        }
    }

    grid_options = gb.build()

    AgGrid(
        df,
        gridOptions=grid_options,
        height=700,
        fit_columns_on_grid_load=False,
        custom_css=custom_css,
        allow_unsafe_jscode=True
    )

    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Sector Stocks CSV",
        csv,
        "sector_inspector.csv",
        "text/csv"
    )

    above20 = (
        df["Above EMA20"] == "✅"
    ).sum()

    total = len(df)

    breadth = round(
        (above20 / total) * 100,
        2
    )

    st.success(
        f"EMA20 Breadth = {breadth}% ({above20}/{total})"
    )