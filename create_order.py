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

# Token list
trade_pair_list = {
    '1': "BTCUSD_PERP",
    '2': "SOLUSD_PERP",
    '3': "ETHUSD_PERP",
    '4': "BNBUSD_PERP",
    '5': "ADAUSD_PERP",
    '6': "DOTUSD_PERP",
    '7': "XRPUSD_PERP",
    '8': "LUNAUSD_PERP",
    '9': "LTCUSD_PERP",
    '10': "LINKUSD_PERP",
    '11': "BCHUSD_PERP",
    '12': "XLMUSD_PERP",
    '13': "EOSUSD_PERP",
    '14': "EGLDUSD_PERP",
    '15': "FILUSD_PERP",
    '16': "ETCUSD_PERP",
    '17': "THETAUSD_PERP",
    '18': "UNIUSD_PERP",
    '19': "TRXUSD_PERP",
    '20': "FTMUSD_PERP",
    '21': "MANAUSD_PERP"
}

# Price of CONT in $
cont_to_usd_list = {
    'BTCUSD_PERP': "100",
    'SOLUSD_PERP': "10",
    'ETHUSD_PERP': "10",
    'BNBUSD_PERP': "10",
    'ADAUSD_PERP': "10",
    'DOTUSD_PERP': "10",
    'XRPUSD_PERP': "10",
    'LUNAUSD_PERP': "10",
    'LTCUSD_PERP': "10",
    'LINKUSD_PERP': "10",
    'BCHUSD_PERP': "10",
    'XLMUSD_PERP': "10",
    'EOSUSD_PERP': "10",
    'EGLDUSD_PERP': "10",
    'FILUSD_PERP': "10",
    'ETCUSD_PERP': "10",
    'THETAUSD_PERP': "10",
    'UNIUSD_PERP': "10",
    'TRXUSD_PERP': "10",
    'FTMUSD_PERP': "10",
    'MANAUSD_PERP': "10"
}

# Max orders per token
orders_total_list = {
    'BTCUSD_PERP': "45",
    'SOLUSD_PERP': "60",
    'ETHUSD_PERP': "12",
    'BNBUSD_PERP': "18",
    'ADAUSD_PERP': "12",
    'DOTUSD_PERP': "18",
    'XRPUSD_PERP': "12",
    'LUNAUSD_PERP': "30",
    'LTCUSD_PERP': "9",
    'LINKUSD_PERP': "4",
    'BCHUSD_PERP': "6",
    'XLMUSD_PERP': "9",
    'EOSUSD_PERP': "1",
    'EGLDUSD_PERP': "9",
    'FILUSD_PERP': "6",
    'ETCUSD_PERP': "3",
    'THETAUSD_PERP': "6",
    'UNIUSD_PERP': "9",
    'TRXUSD_PERP': "6",
    'FTMUSD_PERP': "3",
    'MANAUSD_PERP': "3"
}

# CONT in one order
cont_per_order_list = {
    'BTCUSD_PERP': "1",
    'SOLUSD_PERP': "35",
    'ETHUSD_PERP': "2",
    'BNBUSD_PERP': "3",
    'ADAUSD_PERP': "3",
    'DOTUSD_PERP': "2",
    'XRPUSD_PERP': "2",
    'LUNAUSD_PERP': "4",
    'LTCUSD_PERP': "2",
    'LINKUSD_PERP': "2",
    'BCHUSD_PERP': "2",
    'XLMUSD_PERP': "2",
    'EOSUSD_PERP': "1",
    'EGLDUSD_PERP': "2",
    'FILUSD_PERP': "1",
    'ETCUSD_PERP': "1",
    'THETAUSD_PERP': "2",
    'UNIUSD_PERP': "2",
    'TRXUSD_PERP': "1",
    'FTMUSD_PERP': "2",
    'MANAUSD_PERP': "2"
}

trade_pair = ""

print(trade_pair_list)
try:
    trade_pair = trade_pair_list[str(input("Select token: "))]
except KeyError:
    print("Wrong token number")
    exit()

token = "CONT"
cont_per_order = int(cont_per_order_list[trade_pair])
cont_to_usd = int(cont_to_usd_list[trade_pair])

# Change leverage
min_leverage: int = 2
max_leverage: int = 3
default_leverage: int = 2
set_leverage: int = default_leverage

input_set_leverage: str = input(
    "Set leverage from " + str(min_leverage) + " to " + str(max_leverage) + " [default: " + str(
        default_leverage) + "]: ")

if input_set_leverage != "":
    try:
        set_leverage = int(input_set_leverage)
        if set_leverage < min_leverage:
            print("must be more or equal than", min_leverage)
            exit()
        if set_leverage > max_leverage:
            print("must be less or equal then", max_leverage)
            exit()
    except ValueError:
        print("not number")

print("Set leverage to", set_leverage)

result = request_client.change_initial_leverage(symbol=trade_pair, leverage=set_leverage)
print("===== Change leverage ====")
PrintBasic.print_obj(result)
print("==========================")

result = request_client.get_mark_price(symbol=trade_pair)
print("======= Mark Price =======")
PrintMix.print_data(result)
print("==========================")
current_price: float = result[0].markPrice
print("Current price:", current_price)

print("Trade pair:", trade_pair)
print("Token:", token)
print(cont_to_usd, "USD per 1 CONT")

high_price: float = current_price * 10
input_high_price: str = input("Input max order PRICE (current price $" + str(current_price) + "): ")
try:
    high_price = float(input_high_price)
except ValueError:
    print(input_high_price, "not number")
    exit()
if high_price > current_price:
    print(high_price, "Max price must be less then", current_price)
    exit()

low_price: float = 0.8 * high_price
input_low_price: str = input("Input min order PRICE [default: 80% max price ($" + str(low_price) + ")]: ")

if input_low_price != "":
    try:
        low_price = int(input_low_price)
        if low_price < 0.4 * high_price:
            print("Min price must be more than", 0.4 * high_price)
            exit()
        if low_price > 0.99 * high_price:
            print("Min price must be less then", 0.99 * high_price)
            exit()
    except ValueError:
        print("not number")

recommend_orders: int = int(orders_total_list[trade_pair])
token_total: int = recommend_orders
print("Max orders=320, 1CONT=$" + str(cont_to_usd) + ", " + str(cont_per_order) + " CONT/$" + str(
    cont_per_order * cont_to_usd) + " per order")
input_token_total: str = input("Input number orders [default: " + str(recommend_orders) + " orders / " + str(
    recommend_orders * cont_per_order) + " CONT / $" + str(recommend_orders * cont_per_order * cont_to_usd) + "]")
if input_token_total != "":
    try:
        token_total = int(input_token_total)
        if token_total < 1:
            print("Orders must be more then 0")
            exit()
    except ValueError:
        print("Not a number")
        exit()
high_token_total: int = token_total // 3
# low_token_total = token_total // 3 * 2
low_token_total: int = token_total - high_token_total

if current_price > 1000:
    round_decimal = 0
    format_decimal = "{:.0f}"
elif current_price > 100:
    round_decimal = 1
    format_decimal = "{:.1f}"
elif current_price > 10:
    round_decimal = 2
    format_decimal = "{:.2f}"
elif current_price > 1:
    round_decimal = 3
    format_decimal = "{:.3f}"
elif current_price > 0.1:
    round_decimal = 4
    format_decimal = "{:.4f}"
else:
    round_decimal = 5
    format_decimal = "{:.5f}"
print('round_decimal', round_decimal)
print('format_decimal', format_decimal)

mid_price: float = float(round(low_price + (high_price - low_price) / 2, round_decimal))
low_grid_step: float = float(round((mid_price - low_price) / low_token_total, round_decimal))
high_grid_step: float = float(round((mid_price - low_price) / high_token_total, round_decimal))
print("Total:", cont_per_order * (low_token_total + high_token_total), token, "/",
      cont_to_usd * cont_per_order * (low_token_total + high_token_total), "USD")
print(">>> Low grid:", low_token_total, "orders from", low_price, "to", mid_price, "with step", low_grid_step)
print(">>> High grid:", high_token_total, "orders from", mid_price, "to", high_price, "with step", high_grid_step)

input("Press Enter to continue (Ctrl+D for break)...")

for cont in range(1, low_token_total + 1):
    time.sleep(0.02)
    next_price: str = format_decimal.format(low_price + (cont * low_grid_step))
    print(">>> ", token, " ", cont, ": Price", next_price)
    result = request_client.post_order(symbol=trade_pair, side=OrderSide.BUY, ordertype=OrderType.LIMIT,
                                       price=next_price, quantity=cont_per_order,
                                       timeInForce=TimeInForce.GTC)

for cont in range(1, high_token_total + 1):
    time.sleep(0.02)
    next_price = format_decimal.format(mid_price + (cont * high_grid_step))
    print(">>> ", token, " ", cont, ": Price", next_price)
    result = request_client.post_order(symbol=trade_pair, side=OrderSide.BUY, ordertype=OrderType.LIMIT,
                                       price=next_price, quantity=cont_per_order,
                                       timeInForce=TimeInForce.GTC)

# Get all orders
# result = request_client.get_all_orders(symbol=trade_pair)
# print("==========================")
# PrintMix.print_data(result)
# print("==========================")

print("DONE")
print("==========================")
