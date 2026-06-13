from sector_breadth import get_sector_stocks

sector_map = get_sector_stocks()

for sector, stocks in sector_map.items():

    print()
    print(sector)
    print("Stocks:", len(stocks))