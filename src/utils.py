import requests
import pandas as pd
from io import StringIO
import datetime as dt

# https://github.com/kylerod22/siads593-water-sustainability/blob/main/08-rjbest-sungmiki-kylerod-2026winter/src/utils/wiki_scraper.py
def wiki_scraper(
        url="https://en.wikipedia.org/wiki/List_of_rivers_of_South_Africa",
        headers={"User-Agent": "Chrome/107.0.0.0 Safari/537.36"},
        table=1,
):
    '''
    Scrape a table from URL

    input
    -----
    url: str - pass in any address where there is/are a/tables present
    headers: dict - https://requests.readthedocs.io/en/latest/
    table: int - tables from the url requested are indexed 0 to ...

    return
    ------
    table from url: pd.DataFrame
    '''

    # Wikipedia URL
    url = url

    # Send HTTP request with headers
    response = requests.get(url, headers=headers)

    # Read HTML tables from the response content
    tables = pd.read_html(StringIO(response.text))

    # the second table happens to be where it's at
    df = tables[table]

    # clean columns
    df.columns = df.columns.str.strip().str.lower()

    return df


def write_scraped_df(
        d: dict,
        path: str='../../assets/',
        file_date: str=str(dt.date.today())
):
    '''
    write scraped tables (all same format) from multiple URLs from a defined python dictionary

    input
    -----
    d: dict with description as keys and URLs as values
    path: path to directory
    file_data: date with which data is associated
    '''

    for k, url in d.items():
        
        wiki_scraper(
            url=url,
        ).to_csv(f'{path}{k}_{file_date}.csv', index=False)



def add_liga_col(
        df: pd.DataFrame,
        liga: str
) -> pd.DataFrame:
    '''
    add column to dataframe passed as a parameter with each value named as defined 2nd parameter

    input
    -----
    df: pd.DataFrame
    liga: string to be in each row of the added column

    return
    ------
    pd.DataFrame with added column
    '''
    df.loc[:, 'liga'] = liga
    return df


def concat_scrape(
        liga_dict: dict,
        path: str='../../assets/',

) -> pd.DataFrame:
    '''
    read and concatenate values of a dictionary with a specified path

    input
    -----
    liga_dict: dict
    path: path to directory

    return
    ------
    pd.DataFrame with added column
    '''
    # concatenate scraped data
    df_list = []
    for liga, url in liga_dict.items():
        df_list.append(add_liga_col(df=pd.read_csv(f'{path}{liga + '_' + str(dt.date.today())}.csv'), liga=liga))

    bl_to_vl = pd.concat(df_list)

    return bl_to_vl
