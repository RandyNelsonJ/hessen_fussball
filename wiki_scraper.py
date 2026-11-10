import requests
import pandas as pd
from io import StringIO

# Scrape a list of rivers from South Africa @ https://en.wikipedia.org/wiki/List_of_rivers_of_South_Africa
# Custom headers to mimic a real browser
def wiki_scraper(
        url="https://en.wikipedia.org/wiki/List_of_rivers_of_South_Africa",
        headers={"User-Agent": "Chrome/107.0.0.0 Safari/537.36"},
        table=1,
        # subset='Mouth / junction coordinates'
):

    # Wikipedia URL
    url = url

    # Send HTTP request with headers
    response = requests.get(url, headers=headers) #https://requests.readthedocs.io/en/latest/

    # Read HTML tables from the response content
    tables = pd.read_html(StringIO(response.text))

    # the second table happens to be where it's at
    df = tables[table]#.dropna(subset=subset)

    # clean columns
    df.columns = df.columns.str.strip().str.lower()

    return df