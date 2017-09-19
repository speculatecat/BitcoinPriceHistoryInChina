# -*- coding: utf-8 -*-
# ProjectName   : BitcoinPriceHistoryInChina
# File          : collect_okcoin.py
# Time          : 2017/9/19 14:19
# License       : Copyright(C), YanWong
# Author        : YanWong (speculate_cat)
# Email         : developer.yan.wong@gmail.com
# Description   : This program is collecting daily prices of bitcoin,litecoin,eth,etc,bcc at okcoin.cn,
#                 and store as csv file in
#                 ./data/okcoin/ directory.
# Reference     : https://www.okcoin.cn/rest_api.html
#                 https://github.com/OKCoin/rest/tree/master/python

import http.client
import json
import pandas as pd

REQUEST_URL = 'www.okcoin.cn'
KLINE_TT_COLS = ['date', 'open', 'high', 'low', 'close', 'volume']


def http_get(url, resource, params=''):
    conn = http.client.HTTPSConnection(url, timeout=10)
    conn.request("GET", resource + '?' + params)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    return json.loads(data)


def ticker(symbol='', data_type='1day', since=''):
    ticker_resource = "/api/v1/kline.do"
    params = ''
    if symbol:
        params = 'symbol=%(symbol)s&type=%(type)s' % {'symbol': symbol, 'type': data_type}
    if since:
        params += '&since=%(since)s' % {'since': since}
    k_data = http_get(REQUEST_URL, ticker_resource, params)
    if len(k_data) == 0:
        raise ValueError('Can not obtain the data.')
    else:
        df = pd.DataFrame(k_data, columns=KLINE_TT_COLS)
        df['date'] = pd.to_datetime(df['date'], unit='ms')
    return df


if __name__ == '__main__':
    # okcoin.cn bitcoin - cny since 2013-6-11 ~ now, daily price history
    daily_price_btc_cny = ticker('btc_cny')
    daily_price_btc_cny.to_csv('./data/okcoin/daily_price_btc_cny.csv')
    # okcoin.cn litecoin - cny since 2013-9-11 ~ now daily price history
    daily_price_ltc_cny = ticker('ltc_cny')
    daily_price_ltc_cny.to_csv('./data/okcoin/daily_price_ltc_cny.csv')
    # okcoin.cn eth - cny since 2017-5-31 ~ now daily price history
    daily_price_eth_cny = ticker('eth_cny')
    daily_price_ltc_cny.to_csv('./data/okcoin/daily_price_eth_cny.csv')
    # okcoin.cn etc - cny since 2017-7-16 ~ now daily price history
    daily_price_etc_cny = ticker('etc_cny')
    daily_price_etc_cny.to_csv('./data/okcoin/daily_price_etc_cny.csv')
    # okcoin.cn bcc - cny since 2017-7-16 ~ now daily price history
    daily_price_bcc_cny = ticker('etc_cny')
    daily_price_bcc_cny.to_csv('./data/okcoin/daily_price_bcc_cny.csv')
    # okcoin.cn bitcoin - cny since 2013-6-11 ~ now, hour price history
    hour_price_btc_cny = ticker(symbol='btc_cny', data_type='1hour')
    hour_price_btc_cny.to_csv('./data/okcoin/hour_price_btc_cny.csv')
    # okcoin.cn litecoin - cny since 2013-6-11 ~ now, hour price history
    hour_price_ltc_cny = ticker(symbol='ltc_cny', data_type='1hour')
    hour_price_ltc_cny.to_csv('./data/okcoin/hour_price_ltc_cny.csv')