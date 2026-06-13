import yfinance as yf

stock = "RELIANCE.NS"

df = yf.download(
    stock,
    period="1y",
    auto_adjust=True
)

print(df.tail())
print(df.columns)
print(len(df))