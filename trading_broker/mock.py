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
        self.today_date, self.direction = self.__get_today_date()

    def get_asset_to_trade(self) -> str:
        return self.__asset_to_trade

    def set_asset_to_trade(self, asset_to_trade: str):
        self.__asset_to_trade = asset_to_trade

    def get_current_funds(self) -> float:
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM mock.funds')
            res, = cursor.fetchone()

            return res

    def get_asset_price(self) -> float:
        with self.conn.cursor() as cursor:
            cursor.execute(f'''
                select
                    {self.direction}
                from
                    test_data.niftybees
                where
                    date='{self.today_date}'
            ''')
            res = cursor.fetchone()

            return res[0]

    def get_current_quantity(self) -> int:
        pass

    def buy(self, quantity: int):
        trade_price = self.get_asset_price() * quantity

        with self.conn.cursor() as cursor:
            cursor.execute(f'UPDATE mock.funds SET funds = funds - {trade_price}')

            self.conn.commit()

        return quantity, trade_price

    def sell(self, quantity: int):
        pass

    def __get_today_date(self) -> (str, str):
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT curr_date, direction FROM mock.iterator')
            curr_date, direction = cursor.fetchone()

        with self.conn.cursor() as cursor:
            cursor.execute(f'''
            UPDATE mock.iterator
            SET curr_date = (select date from test_data.niftybees where date > '{curr_date}' order by date limit 1),
                direction = '{'close' if direction == 'open' else 'open'}'
            ''')

            self.conn.commit()

        return curr_date, direction
