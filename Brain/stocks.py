import json
from urllib import request
import requests
import pandas as pd
from load_key_from_config import getConfigKey

stock_keyword_list = ["Stock", "stock", "trading", "stock price", "share price"]

def load_ticker(org_entity):
    try:
        mapping_df = pd.read_csv('C:/Users/syeda/VA/venv/Scripts/Vision-The-Virtual-Assistant/Database/nasdaq_company_list.csv')
        ticker_symbol = mapping_df[mapping_df['Name'].str.contains(org_entity, case=False)]['Symbol'].values[0]
        return ticker_symbol
    except:
        return f"Error: Could not find ticker symbol for {org_entity} in NASDAQ Database.\n\n"


def getStocks(company_name):
    ticker = load_ticker(company_name)
    if 'Error' in ticker:
        return ticker

    api_key = getConfigKey("stocksAPI")
    stockdata = get_stock_quote(ticker, api_key)
    stock_price = get_stock_price(ticker, api_key)
    return stockdata
def get_stock_price(ticker_symbol, api):
    url = f"https://api.twelvedata.com/price?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    price = response['price'][:-3]
    return price


def get_stock_quote(ticker_symbol, api):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    return response


# exchange = stockdata['exchange']
# currency = stockdata['currency']
# open_price = stockdata['open']
# high_price = stockdata['high']
# low_price = stockdata['low']
# close_price = stockdata['close']
# volume = stockdata['volume']
