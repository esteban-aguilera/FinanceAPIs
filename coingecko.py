import numpy as np
import pandas as pd
import requests

# package libraries
from utils import extract_pairs, list_to_string


# --------------------------------------------------------------------------------
# constants
# --------------------------------------------------------------------------------
BASE_URL = 'https://api.coingecko.com/api/v3'


# --------------------------------------------------------------------------------
# functions
# --------------------------------------------------------------------------------
def main():
    pairs = [('bitcoin', 'usd'), ('ethereum', 'usd')]
    dates = ['12-10-2015', '13-10-2015']
    
    val = historical_prices(pairs[0], dates)
    print(val)


# --------------------------------------------------------------------------------
# communication with api
# --------------------------------------------------------------------------------
def historical_prices(pair, dates, **kwargs):
    """Get price of a coin/currency pair for a list of dates.

    Parameters
    ----------
    pair: str
        Coin/currency pair.

    dates: list
        Symbol of the base currency

    Returns
    -------
    df: pandas.DataFrame
        DataFrame with the historical price of a coin/currency pair for every
        input date.
    """
    coin, currency = pair
    num = len(dates)
    
    # create empty DataFrame
    columns = list( historical_price((coin, currency), dates[0]) )
    df = pd.DataFrame(np.zeros([num, 3]), index=dates, columns=columns)

    for date in dates:
        values = historical_price((coin, currency), date)
        
        for col in columns:
            df.loc[date, col] = values[col]

    return df


def historical_price(pair, date, currency=None):
    """Get price of a coin in a particular date.

    Parameters
    ----------
    coin: str
        Cryptocurrency name

    date: str
        Date of interest.  Must be formated as dd-mm-yyyy.

    currency: str, optional
        Symbol of the base currency.

    Returns
    -------
    values: dict
        Historical data for the particular pair.  It has the entries
        'current_price', 'market_cap' and 'total_volume'
    """
    columns = ['current_price', 'market_cap', 'total_volume']

    # get url for API request
    coin, currency = pair
    url = f'{BASE_URL}/coins/{coin}/history?date={date}'

    # get request in json and extract market data
    r = requests.get(url).json()
    
    if(list(r)[0] == 'error'):
        raise ValueError(r['error'])
    
    r = r['market_data']
    
    values = {}
    for col in columns:
        values[col] = r[col][currency]

    return values


def current_prices(pairs):
    """Get current price of multiple coins/currencies pair.

    Parameters
    ----------
    coins: list
        List of pairs with the name of the cryptocurrencies and the symbols
        of the base currency.

    Returns
    -------
    values: list
        List with the current prices of the corresponding pairs.

    Example
    -------
    current_prices([('bitcoin', 'usd'), ('ethereum', 'clp')])
        --> [current BTC/USD, current ETH/CLP]
    """
    # extract coins and currencies
    coins, currencies = extract_pairs(pairs)

    # format list as valid strings
    coins_str = list_to_string( np.unique(coins) )
    currencies_str = list_to_string( np.unique(currencies) )
    
    # generate url.
    url = f'{BASE_URL}/simple/price?ids={coins_str}&vs_currencies={currencies_str}'
    
    # get request into a dictionary.
    r = requests.get(url).json()
    
    values = np.zeros(len(pairs))
    for i, pair in enumerate(pairs):
        coin, currency = pair
        values[i] = r[coin][currency]
    
    return values


# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    main()