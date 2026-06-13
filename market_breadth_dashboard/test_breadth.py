from data_fetcher import get_index_constituents
from breadth import calculate_breadth

stocks = get_index_constituents(
    "Nifty Smallcap 250"
)

result = calculate_breadth(
    stocks[:25]
)

print(result)