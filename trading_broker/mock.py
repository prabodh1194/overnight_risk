import logging

import psycopg2

import settings
from trading_broker import TradingBroker

logger = logging.getLogger(__name__)


class MockTradingBroker(TradingBroker):
    def __init__(self):
        self.__asset_to_trade: str = ''
        self.conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password=settings.POSTGRES_PASSWORD
        )

    def set_asset_to_trade(self, asset_to_trade: str):
        self.__asset_to_trade = asset_to_trade

    def get_current_funds(self) -> float:
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM mock.funds')
            res = cursor.fetchone()

            return res

    def get_asset_price(self) -> float:
        pass

    def get_current_quantity(self) -> int:
        pass

    def buy(self, quantity: int):
        pass

    def sell(self, quantity: int):
        pass
