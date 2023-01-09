import psycopg2

import settings
from constants import TradingPartner, TradingDirection
from trading_broker import TradingBroker
from trading_broker.mock import MockTradingBroker
from trading_broker.zerodha import ZerodhaTradingBroker


class BuyTheClose:
    def __init__(self, trading_partner: TradingPartner):
        self.trading_broker: TradingBroker

        if trading_partner == TradingPartner.mock:
            self.trading_broker = MockTradingBroker()
        elif trading_partner == TradingPartner.zerodha:
            self.trading_broker = ZerodhaTradingBroker()

        self.conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password=settings.POSTGRES_PASSWORD
        )

    def run(self, asset_to_trade: str, direction: TradingDirection):
        self.trading_broker.set_asset_to_trade(asset_to_trade)

        if direction == TradingDirection.long:
            self.buy()
        elif direction == TradingDirection.short:
            self.sell()
        else:
            raise ValueError("Invalid direction")

    def buy(self):
        current_funds = self.trading_broker.get_current_funds()
        current_price = self.trading_broker.get_asset_price()

        quantity = int(current_funds // current_price)

        quantity, total_trade_price = self.trading_broker.buy(quantity)

        self.record_trade(TradingDirection.long, quantity, total_trade_price)

    def sell(self):
        current_quantity = self.trading_broker.get_current_quantity()

        self.trading_broker.sell(current_quantity)

    def record_trade(self, direction: TradingDirection, quantity: int, total_trade_price: float):
        with self.conn.cursor() as cursor:
            cursor.execute(f'''
                INSERT INTO trades (open_funds, direction, asset, quantity, price, close_funds)
                            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                self.trading_broker.get_current_funds() + total_trade_price,
                direction,
                self.trading_broker.get_asset_to_trade(),
                quantity,
                total_trade_price,
                self.trading_broker.get_current_funds()
            ))
            self.conn.commit()


if __name__ == '__main__':
    BuyTheClose(TradingPartner.mock).run('NIFTYBEES', TradingDirection.long)
