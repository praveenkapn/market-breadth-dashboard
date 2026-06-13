import pandas as pd
from sector_breadth import get_sector_stocks
from breadth import calculate_breadth

results = []

sector_map = get_sector_stocks()

for sector, stocks in sector_map.items():

    print(f"Processing {sector}")

    result = calculate_breadth(
        stocks
    )

    if result:

        results.append({
            "Sector": sector,
            "Stocks": len(stocks),
            "EMA20": result["EMA20"],
            "EMA20": result["EMA50"],
            "EMA100": result["EMA100"],
            "EMA200": result["EMA200"]
        })

df = pd.DataFrame(results)

df = df.sort_values(
    "EMA20",
    ascending=False
)

print(df)