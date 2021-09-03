#!/usr/bin/env python3

import os

from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
import time
import json

secret_file = open('secrets.json', )
secrets = json.load(secret_file)
secret_file.close()

g_api_key = secrets['binance_api']
g_secret_key = secrets['binance_secret']
g_url = secrets['binance_futures_url']

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key, url=g_url)

trade_pair_list = {
    '1': "BTCUSD_PERP",
    '2': "SOLUSD_PERP"
}

token_list = {
  'BTCUSD_PERP': "CONT",
  'SOLUSD_PERP': "CONT"
}

quantity_per_order_list = {
  'BTCUSD_PERP': "1",
  'SOLUSD_PERP': "20"
}

trade_pair = ""
try:
    trade_pair = trade_pair_list[str(input("1. BTCUSD_PERP, 2. SOLUSD_PERP: "))]
except KeyError:
    print("Wrong number, select 1 or 2")
    exit()

token = token_list[trade_pair]
quantity_per_order = quantity_per_order_list[trade_pair]

print("Trade pair:", trade_pair)
print("Token:", token)

# Change leverage
min_leverage = 2
max_leverage = 3
set_leverage = 2

try:
    set_leverage = int(input("Set leverage from 2 to 3: "))
except ValueError:
    print("not number")
    exit()

if set_leverage < min_leverage:
    print(set_leverage, "must be more or equal than", min_leverage)
    exit()

if set_leverage > max_leverage:
    print(set_leverage, "must be less or equal then", max_leverage)
    exit()

print("Set leverage to", set_leverage)

result = request_client.change_initial_leverage(symbol=trade_pair, leverage=set_leverage)
print("===== Change leverage ====")
PrintBasic.print_obj(result)
print("==========================")

result = request_client.get_mark_price(symbol=trade_pair)
print("======= Mark Price =======")
PrintMix.print_data(result)
print("==========================")
current_price = result[0].markPrice
print("Current price:", current_price)

input_high_price = input("Input max order PRICE (current price " + str(current_price) + "$): ")
try:
    high_price = int(input_high_price)
except ValueError:
    print(input_high_price, "not number")
    exit()
if high_price > current_price:
    print(high_price, "must be less then", current_price)
    exit()

input_low_price = input("Input min order PRICE: ")
try:
    low_price = int(input_low_price)
except ValueError:
    print(input_low_price, "not number")
    exit()
if low_price > high_price:
    print(low_price, "must be less then", high_price)
    exit()

token_total = 0
try:
    token_total = int(input("Input number orders (max 320 orders, "+quantity_per_order+token+" in 1 order): "))
except ValueError:
    print("Not a number")
    exit()
if token_total < 1:
    print(token_total, "must be more then 0")
    exit()
low_token_total = token_total // 3 * 2
high_token_total = token_total // 3

mid_price = float(round(low_price + (high_price - low_price) / 2, 2))
low_grid_step = float(round((mid_price - low_price) / low_token_total, 2))
high_grid_step = float(round((mid_price - low_price) / high_token_total, 2))
print(">>> Low grid:", low_token_total, " orders from ", low_price, " to ", mid_price, " with step ", low_grid_step)
print(">>> High grid:", high_token_total, " orders from ", mid_price, " to ", high_price, " with step ", high_grid_step)

input("Press Enter to continue...")

decimal_count = 2

for cont in range(1, low_token_total + 1):
    time.sleep(0.02)
    next_price = "{:.1f}".format(low_price + (cont * low_grid_step))
    # next_price2 = f"{float(low_price + (cont * low_grid_step)):.{decimal_count}f}"
    print(">>> ", token, " ", cont, ": Price", next_price)
    result = request_client.post_order(symbol=trade_pair, side=OrderSide.BUY, ordertype=OrderType.LIMIT,
                                       price=next_price, quantity=int(quantity_per_order), timeInForce=TimeInForce.GTC)

for cont in range(1, high_token_total + 1):
    time.sleep(0.02)
    next_price = "{:.1f}".format(mid_price + (cont * high_grid_step))
    # next_price = f"{float(mid_price + (cont * high_grid_step)):.{decimal_count}f}"
    print(">>> ", token, " ", cont, ": Price", next_price)
    result = request_client.post_order(symbol=trade_pair, side=OrderSide.BUY, ordertype=OrderType.LIMIT,
                                       price=next_price, quantity=int(quantity_per_order), timeInForce=TimeInForce.GTC)

# Get all orders
# result = request_client.get_all_orders(symbol=trade_pair)
# print("==========================")
# PrintMix.print_data(result)
# print("==========================")

print("DONE")
print("==========================")
