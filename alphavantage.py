import pandas as pd
import requests

from datetime import datetime


# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
def main():
    """Example on how to run this functions
    """
    # get daily data
    df = get_daily('AAPL', 'ALPHAVANTAGE_KEY')
    print(df, '\n\n')
    
    # get hourly data
    df = get_intraday('AAPL', 'ALPHAVANTAGE_KEY', 60)
    print(df)


# --------------------------------------------------------------------------------
# functions
# --------------------------------------------------------------------------------
def get_daily(symbol, apikey):
    """Get daily OHLC data from AlphaVantage.

    ----------
    symbol: str
        Stock market symbol.

    apikey: str
        API key used to access AlphaVantage.

    Returns
    -------
    df: pandas.DataFrame
        DataFrame with all the information of the specified symbol.
    """
    df = _get_ohlc(symbol, apikey, 1440)

    return df


def get_intraday(symbol, apikey, interval):
    """Get intraday OHLC data from AlphaVantage.

    ----------
    symbol: str
        Stock market symbol.

    apikey: str
        API key used to access AlphaVantage.

    interval: int
        Time in minutes used to obtain the OHLC data.  It can be [1, 5, 15,
        30, 60]

    Returns
    -------
    df: pandas.DataFrame
        DataFrame with all the information of the specified symbol.
    """
    if(interval in [1, 5, 15, 30, 60]):
        df = _get_ohlc(symbol, apikey, 1440)
    else:
        raise Exception(f'{interval} is invalid interval for intraday. Valid intervals: [1, 5, 15, 30, 60]')
   
    return df


# --------------------------------------------------------------------------------
# communication with API
# --------------------------------------------------------------------------------
def _get_ohlc(symbol, apikey, interval):
    """Get daily or intraday data from AlphaVantage.

    ----------
    symbol: str
        Stock market symbol.

    apikey: str
        API key used to access AlphaVantage.

    interval: int
        Time in minutes used to obtain the OHLC data.  It can be [1, 5, 15,
        30, 60, 1440]

    Returns
    -------
    df: pandas.DataFrame
        DataFrame with all the information of the specified symbol.
    """    
    # generate url
    if(interval == 1440):  # daily
        url = f'https://www.alphavantage.co/query?' + \
            f'function=TIME_SERIES_DAILY_ADJUSTED&' + \
            f'symbol={symbol}&' + \
            f'outputsize=full&' + \
            f'apikey={apikey}'
        fmt = '%Y-%m-%d'
    elif(interval in [1, 5, 15, 30, 60]):  # intraday
        url = f'https://www.alphavantage.co/query?' + \
            f'function=TIME_SERIES_INTRADAY&' + \
            f'symbol={symbol}&' + \
            f'interval={interval}min&' + \
            f'outputsize=full&' + \
            f'apikey={apikey}'
        fmt = '%Y-%m-%d %H:%M:%S'
    else:
        raise Exception(f'{interval} is invalid interval. Valid intervals: [1, 5, 15, 30, 60, 1440]')
    
    # get data from url
    r = requests.get(url)
    r = r.json()
    
    # check if there was an error in the request
    if('Error Message' in list(r)):
        raise Exception(r['Error Message'])
    
    # if there was no error.  Extract the data
    col = list(r)[1]
    r = r[col]
    
    # transform dictionary to DataFrame
    df = pd.DataFrame.from_dict(r, orient='index')

    # erase spaces from columns names and replace them by underscores.
    df.columns = ['_'.join(col.split()[1:]) for col in df.columns]
    # change datetime format to unix timestamp.
    df['created_at'] = [datetime.strptime(idx, fmt).timestamp()
                        for idx in df.index.values]
    # reorder columns so that 'created_at' appear first.
    df = df[[df.columns[-1]] + df.columns[:-1].tolist()]

    # sort rows by 'created_at' column.
    df = df.sort_values(by='created_at')

    # reset and format DataFrame index
    df = df.reset_index(drop=True)
    
    # change types of each column in the dataframe
    for col in df.columns:
        if(col in ['created_at']):
            df[col] = df[col].astype(int)
        else:
            df[col] = pd.to_numeric(df[col])

    return df


# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    main()