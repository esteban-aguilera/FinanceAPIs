import os

# package imports
from finance_apis import alphavantage, coingecko

# get APIs keys
import secrets

# --------------------------------------------------------------------------------
# constants
# --------------------------------------------------------------------------------
ALPHAVANTAGE_APIKEY = os.environ.get('ALPHAVANTAGE_APIKEY')


# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
def main():
    """Example on how to run the functions in this file.  The user must get a
    AlphaVatange key before using this library.
    """    
    df = alphavantage.get_daily('AAPL', ALPHAVANTAGE_APIKEY)
    print('AlphaVantage daily data:')
    print(df, 2*'\n')
    
    df = alphavantage.get_intraday('AAPL', ALPHAVANTAGE_APIKEY, 60)
    print('AlphaVantage hourly data:')
    print(df, 3*'\n')

    # test CoinGecko
    pairs = [('bitcoin', 'usd'), ('ethereum', 'usd')]
    dates = ['12-10-2015', '13-10-2015']
    
    val = coingecko.historical_prices(pairs[0], dates)
    print('CoinGecko Historical Prices')
    print(val)


# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    main()