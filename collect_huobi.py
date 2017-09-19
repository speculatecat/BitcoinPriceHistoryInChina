# -*- coding: utf-8 -*-
# ProjectName   : BitcoinPriceHistoryInChina
# File          : collect_huobi.py
# Time          : 2017/9/19 15:11
# License       : Copyright(C), YanWong
# Author        : YanWong (speculate_cat)
# Email         : developer.yan.wong@gmail.com
# Description   : This program is collecting daily prices of bitcoin,litecoin at huobi.com,
#                 and store as csv file in
#                 ./data/huobi/ directory.
# Reference     : https://github.com/huobiapi/API_Docs/wiki/REST-Interval

import http.client
import json
import pandas as pd

REQUEST_URL = 'api.huobi.com'
KLINE_TT_COLS = ['date', 'open', 'high', 'low', 'close', 'volume']


def http_get(url, resource, params=''):
    conn = http.client.HTTPSConnection(url, timeout=10)
    conn.request("GET", resource + '?' + params)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    return json.loads(data)


def ticker(symbol=''):
    ticker_resource = "/staticmarket/%(symbol)s_kline_100_json.js" % {'symbol': symbol}
    params = ''
    if symbol:
        params = 'length=2000'
    k_data = http_get(REQUEST_URL, ticker_resource, params)
    if len(k_data) == 0:
        raise ValueError('Can not obtain the data.')
    else:
        df = pd.DataFrame(k_data, columns=KLINE_TT_COLS)
        df['date'] = pd.to_datetime(df['date'], format="%Y%m%d%H%M%S%f")
    return df

if __name__ == '__main__':
    # huobi.com bitcoin - cny since 2013-9-1 ~ now, daily price history
    daily_price_btc_cny = ticker('btc')
    daily_price_btc_cny.to_csv('./data/huobi/daily_price_btc_cny.csv')
    # huobi.com litecoin - cny since 2014-3-9 ~ now daily price history
    daily_price_ltc_cny = ticker('ltc')
    daily_price_ltc_cny.to_csv('./data/huobi/daily_price_ltc_cny.csv')