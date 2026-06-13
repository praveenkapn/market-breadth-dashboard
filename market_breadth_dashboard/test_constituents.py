from data_fetcher import get_index_constituents

stocks = get_index_constituents("Nifty Smallcap 250")

print(f"Total Stocks: {len(stocks)}")

print(stocks[:20])