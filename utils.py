import requests
import pandas as pd
from io import StringIO

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


def write_scraped_df(
        d: dict=liga_dict,
        file_date: str='20261103' # try str(dt.today())
):
    '''
    write scrapped tables (all same format) from multiple URLs from a defined python dictionary

    input
    -----
    d: dict with description as keys and URLs as values

    '''

    for k, url in d.items():
        
        wiki_scraper.wiki_scraper(
            url=url,
        ).to_csv(f'assets/{k}_{file_date}.csv', index=False)



def add_liga_col(df, liga):
    df.loc[:, 'liga'] = liga
    return df
