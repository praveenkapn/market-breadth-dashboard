import pandas as pd
import requests
from io import StringIO

url = "https://www.niftyindices.com/IndexConstituent/ind_nifty500list.csv"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers,
    timeout=60
)

df = pd.read_csv(
    StringIO(response.text)
)

print(df.columns)

print()

print(df.head())