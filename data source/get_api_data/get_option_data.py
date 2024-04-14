# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 19:57:59 2024

@author: jdl
"""

import pandas as pd
import datetime
import rqdatac
import download_util


rqdatac.init('license', download_util.key)


# =============================================================================
# get option data
# =============================================================================

start_date = '2015-01-01'
today_date = pd.to_datetime(datetime.date.today())
today_date = today_date.strftime('%Y-%m-%d')


# get option info
option_info = rqdatac.all_instruments(type='Option', market='cn', date=None)
option_info.to_pickle('option_data/option_info')

# get exchange code
trade_code = rqdatac.id_convert(option_info['order_book_id'].to_list(),to='normal')
code_map = pd.Series(index=option_info['order_book_id'].to_list(), data=trade_code)
code_map.name = 'trade_code'
code_map.to_pickle('option_data/code_map')


# get option eod
calculate_option = option_info[option_info['maturity_date'] >= start_date]
option_ids = list(calculate_option['order_book_id'].unique())
field_param = ['open','high','low','close','total_turnover','volume','open_interest']
option_eod = rqdatac.get_price(option_ids, start_date=start_date, end_date=today_date, 
                                  frequency='1d', fields=field_param, adjust_type='none', 
                                  skip_suspended =False, market='cn', expect_df=True,time_slice=None)
option_eod.to_pickle('option_data/option_eod')


# get underlying eod
underlying_id = list(option_info['underlying_order_book_id'].unique())
field_param = ['open','close','low','high','volume']
underlying_close = rqdatac.get_price(underlying_id, start_date=start_date, end_date=today_date, 
                                  frequency='1d', fields=field_param, adjust_type='none', 
                                  skip_suspended =False, market='cn', expect_df=True,time_slice=None)
underlying_close.to_pickle('option_data/underlying_eod')


# get option geeks
field_param = ['iv','Delta','Gamma','Vega','Theta','Rho']
option_greeks = rqdatac.options.get_greeks(order_book_ids =  option_ids, start_date = start_date, end_date = today_date,
                            fields=None, model='implied_forward',price_type='close')
option_greeks.to_pickle('option_data/option_greeks')



# =============================================================================
# get index data
# =============================================================================

# get index info
index_info = rqdatac.all_instruments(type='INDX', market='cn', date=None)
index_info.to_pickle('index_data/index_info')


# get exchange code
trade_code = rqdatac.id_convert(index_info['order_book_id'].to_list(),to='normal')
code_map = pd.Series(index=index_info['order_book_id'].to_list(), data=trade_code)
code_map.name = 'trade_code'
code_map.to_pickle('index_data/code_map')


# get index eod
start_date = '2019-01-01'
index_ids = list(index_info['order_book_id'].unique())
field_param = ['open','high','low','close','volume']
index_eod = rqdatac.get_price(index_ids, start_date=start_date, end_date=today_date, 
                                  frequency='1d', fields=field_param, adjust_type='none', 
                                  skip_suspended =False, market='cn', expect_df=True,time_slice=None)
index_eod.to_pickle('index_data/index_eod')



# =============================================================================
# get news demo
# =============================================================================
news = rqdatac.get_current_news(start_time='2021-03-01 00:00:00', end_time='2021-03-31 00:00:00')
news.to_pickle('news_demo')




# =============================================================================
# get future data
# =============================================================================

# get future info
future_info = rqdatac.all_instruments(type='Future', market='cn', date=None)
future_info.to_pickle('future_data/future_info')


# get exchange code
trade_code = rqdatac.id_convert(future_info['order_book_id'].to_list(),to='normal')
code_map = pd.Series(index=future_info['order_book_id'].to_list(), data=trade_code)
code_map.name = 'trade_code'
code_map.to_pickle('future_data/code_map')



# get future eod
start_date = '2019-01-01'
future_ids = list(future_info['order_book_id'].unique())

field_param = ['open','high','low','close','volume']
future_eod = rqdatac.get_price(future_ids, start_date=start_date, end_date=today_date, 
                                  frequency='1d', fields=field_param, adjust_type='none', 
                                  skip_suspended =False, market='cn', expect_df=True,time_slice=None)
index_eod.to_pickle('future_data/future_eod')






