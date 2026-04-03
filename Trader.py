from datamodel import OrderDepth, UserId, TradingState, Order, Trade
from typing import List
import numpy as np
import string

MAX_POS = 80

HIST_T_DATA = {
    "HIST_AVG_TRADE_PRICE" : 4992.571951219512,
    "HIST_STD_TRADE_PRICE" : 21.117578935455207,
    "HIST_SIZE" : 820
}

HIST_E_DATA = {
    "HIST_AVG_TRADE_PRICE" : 9999.799498746866,
    "HIST_STD_TRADE_PRICE" : 7.886405278701014,
    "HIST_SIZE" : 399
}

HIST_DATA = {
    "TOMATOES" : HIST_T_DATA,
    "EMERALDS" : HIST_E_DATA
}

class Trader:

    def bid(self):
        return 15

    def scaled_sigmoid(self,c,k,x):
        """Sigmoid with amplitude c-k and height k"""
        return c/(1+np.exp(-x)) + k

    def _calc_pnl(self, past_trades: list[Trade], position, price):
        realized_pnl = 0
        for trade in past_trades:
            if trade.buyer == "SUBMISSION":
                realized_pnl += -trade.price * trade.quantity
                print(f"Past long position cash: {realized_pnl}")
            else:
                realized_pnl += trade.price * trade.quantity
                print(f"Past short position cash: {realized_pnl}")
        unrealized_pnl = position * price
        return realized_pnl + unrealized_pnl

    # def _get_data(self, product, state: TradingState):
    #     avg_price = HIST_DATA[product]["HIST_AVG_TRADE_PRICE"]
    #     std_price = HIST_DATA[product]["HIST_STD_TRADE_PRICE"]
    #     order_depth = state.order_depths[product]
    #     position = state.position[product]
    #     own_trades = state.own_trades[product]
    #     market_trades = state.market_trades[product]
    #     timestamp = state.timestamp[product]
    #     return avg_price, std_price, order_depth, position, own_trades, market_trades, timestamp
    
    def _t_strategy(self, product, state):
        # avg_price, _, order_depth, position, own_trades, market_trades, timestamp = self._get_data(product, state)
        orders: list[Trade] = []
        return orders

    def _e_strategy(self, product, state: TradingState):
        order_depth = state.order_depths[product]
        orders: list[Trade] = []
        sells = order_depth.sell_orders
        buys = order_depth.buy_orders

        best_bid = max(buys.keys())
        best_ask = min(sells.keys())
        mid_price = (best_bid + best_ask) / 2
        
        fair_price = mid_price
        print(fair_price)

        try:
            own_trades = state.own_trades[product]
            position = state.position[product]
            pnl = self._calc_pnl(own_trades, position, fair_price)
            print(f"PnL: {pnl}")
        except: 
            print("There are no past trades yet")


        if len(sells) != 0:
            for sell in sells.items():
                (price, qty) = sell
                print(f"Sell price: {price} - quantity: {qty}")
                if price < fair_price:
                    print("BUY", str(qty) + "x", price)
                    orders.append(Order(product, price, -qty))
        
        if len(buys) != 0:
            for buy in buys.items():
                (price, qty) = buy
                print(f"Buy price: {price} - quantity: {qty}")
                if price > fair_price:
                    print("SELL", str(qty) + "x", price)
                    orders.append(Order(product, price, -qty))

        return orders

    
    def run(self, state: TradingState):
        """Only method required. It takes all buy and sell orders for all
        symbols as an input, and outputs a list of orders to be sent."""
        # Orders to be placed on exchange matching engine
        result = {}
        orders_e = self._e_strategy("EMERALDS", state)
        orders_t = self._t_strategy("TOMATOES", state)

        # order_depth: OrderDepth = state.order_depths[product]
        # orders: List[Order] = []
        # position = state.position[product]

        # avg_price = HIST_DATA[product]["HIST_AVG_TRADE_PRICE"]
        # std_price = HIST_DATA[product]["HIST_STD_TRADE_PRICE"]

        # if len(order_depth.sell_orders) != 0:
        #     best_ask = min(list(order_depth.sell_orders.keys()))
        # else:
        #     best_ask = 0

        # if len(order_depth.buy_orders) != 0:
        #     best_bid = max(list(order_depth.buy_orders.keys()))
        # else:
        #     best_bid = 0

        # spread = best_ask - best_bid
        # mid_price = (best_bid + best_ask) / 2

        # buy_volume = sum(order_depth.buy_orders.values())
        # sell_volume = -sum(order_depth.sell_orders.values())
        # market_pressure = (buy_volume - sell_volume) / (buy_volume + sell_volume)

        # std_avg_ratio = std_price/avg_price
        # weight = self.scaled_sigmoid(2*std_avg_ratio, 1-std_avg_ratio, market_pressure) # No lo usamos ahora

        # acceptable_price = 10
        # pnl = self._calc_pnl(state.own_trades[product], position, acceptable_price)
        # print(pnl)

        # print(f"Mid price: {mid_price}")
        # print(f"Std price: {std_price}")
        # print(f"Market pressure: {market_pressure}")
        # print(f"Weight: {weight}")
        # print("Acceptable price : " + str(acceptable_price))
        # print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

        # if len(order_depth.sell_orders) != 0:
        #     best_ask_amount = order_depth.sell_orders[min(list(order_depth.sell_orders.keys()))]
        #     if int(best_ask) < acceptable_price:
        #         print("BUY", str(-best_ask_amount) + "x", best_ask)
        #         orders.append(Order(product, best_ask, -best_ask_amount))

        # if len(order_depth.buy_orders) != 0:
        #     best_bid_amount = order_depth.buy_orders[max(list(order_depth.buy_orders.keys()))]
        #     if int(best_bid) > acceptable_price:
        #         print("SELL", str(best_bid_amount) + "x", best_bid)
        #         orders.append(Order(product, best_bid, -best_bid_amount))

        result["EMERALDS"] = orders_e
        result["TOMATOES"] = orders_t
    
        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
        # Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData
    
