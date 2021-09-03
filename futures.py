import os

from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *

g_api_key = os.environ.get('binance_api')
g_secret_key = os.environ.get('binance_secret')
g_url = os.environ.get('binance_futures_url')

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key, url=g_url)

result = request_client.get_mark_price(symbol="BTCUSDT")

print("======= Mark Price =======")
PrintBasic.print_obj(result)
print("==========================")
members = [attr for attr in dir(result) if not callable(attr) and not attr.startswith("__")]
for member_def in members:
    if member_def == 'markPrice':
      val_str = str(getattr(result, member_def))
      #print(val_str)
print("==========================")
print(str(getattr(result, 'markPrice')))
print("==========================")
    

#get_all_orders

from binance_f.model.constant import *

result = request_client.get_all_orders(symbol="BTCUSDT")
PrintMix.print_data(result)



result = request_client.get_symbol_price_ticker()
#result = request_client.get_symbol_price_ticker(symbol="BTCUSDT")

print("======= Symbol Price Ticker =======")
PrintMix.print_data(result)
print("===================================")