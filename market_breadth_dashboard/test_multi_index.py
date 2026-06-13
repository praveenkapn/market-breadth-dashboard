from data_fetcher import get_index_constituents
from breadth import calculate_breadth

indices = [
    "Nifty 50",
    "Nifty 500",
    "Nifty Midcap 150",
    "Nifty Smallcap 250"
]

for idx in indices:

    print(f"\nProcessing {idx}")

    stocks = get_index_constituents(idx)

    result = calculate_breadth(
        stocks[:25]
    )

    print(result)