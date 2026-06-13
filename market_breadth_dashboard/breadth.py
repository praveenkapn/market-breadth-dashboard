import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=1800)
def calculate_breadth(symbols):

    try:

        data = yf.download(
            symbols,
            period="1y",
            auto_adjust=False,
            progress=False,
            threads=True
        )

        above20 = 0
        above50 = 0
        above100 = 0
        above200 = 0

        processed = 0

        for symbol in symbols:

            try:

                if len(symbols) == 1:
                    close = data["Close"]
                else:
                    close = data["Close"][symbol]

                close = close.dropna()

                if len(close) < 200:
                    continue

                current = float(close.iloc[-1])

                ema20 = float(
                    close.ewm(
                        span=20,
                        adjust=False
                    ).mean().iloc[-1]
                )

                ema50 = float(
                    close.ewm(
                        span=50,
                        adjust=False
                    ).mean().iloc[-1]
                )

                ema100 = float(
                    close.ewm(
                        span=100,
                        adjust=False
                    ).mean().iloc[-1]
                )

                ema200 = float(
                    close.ewm(
                        span=200,
                        adjust=False
                    ).mean().iloc[-1]
                )

                processed += 1

                if current > ema20:
                    above20 += 1

                if current > ema50:
                    above50 += 1

                if current > ema100:
                    above100 += 1

                if current > ema200:
                    above200 += 1

            except Exception:
                continue

        if processed == 0:
            return None

        return {
            "Processed": processed,
            "EMA20": round((above20 / processed) * 100, 2),
            "EMA50": round((above50 / processed) * 100, 2),
            "EMA100": round((above100 / processed) * 100, 2),
            "EMA200": round((above200 / processed) * 100, 2)
        }

    except Exception:
        return None

@st.cache_data(ttl=900)
def get_stock_details(symbols, stocks):

    rows = []

    try:

        data = yf.download(
            symbols,
            period="5y",
            auto_adjust=False,
            progress=False,
            threads=True
        )

        for symbol in symbols:

            try:

                if len(symbols) == 1:
                    close = data["Close"]
                else:
                    close = data["Close"][symbol]

                close = close.dropna()

                if len(close) < 200:
                    continue

                current = float(close.iloc[-1])

                ema20 = float(
                    close.ewm(
                        span=20,
                        adjust=False
                    ).mean().iloc[-1]
                )

                ema50 = float(
                    close.ewm(
                        span=50,
                        adjust=False
                    ).mean().iloc[-1]
                )

                ema100 = float(
                    close.ewm(
                        span=100,
                        adjust=False
                    ).mean().iloc[-1]
                )

                ema200 = float(
                    close.ewm(
                        span=200,
                        adjust=False
                    ).mean().iloc[-1]
                )

                company_name = next(
                    (
                        s["company"]
                        for s in stocks
                        if s["symbol"] == symbol
                    ),
                    ""
                )

                rows.append({
                    "Company Name": company_name,
                    "Stock Symbol": symbol.replace(".NS", ""),
                    "Price": round(current, 2),

                    "EMA20": round(ema20, 2),
                    "EMA50": round(ema50, 2),
                    "EMA100": round(ema100, 2),
                    "EMA200": round(ema200, 2),

                    "Diff20": round(current - ema20, 2),
                    "Diff50": round(current - ema50, 2),
                    "Diff100": round(current - ema100, 2),
                    "Diff200": round(current - ema200, 2),

                    "Above EMA20": "✅" if current > ema20 else "❌",
                    "Above EMA50": "✅" if current > ema50 else "❌",
                    "Above EMA100": "✅" if current > ema100 else "❌",
                    "Above EMA200": "✅" if current > ema200 else "❌"
                })

            except Exception:
                continue

        return pd.DataFrame(rows)

    except Exception:

        return pd.DataFrame()
