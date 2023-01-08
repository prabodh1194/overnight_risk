from abc import ABC, abstractmethod

from constants import TradingPartner, TradingDirection
from trading_broker.mock import MockTradingBroker
from trading_broker.zerodha import ZerodhaTradingBroker


class TradingBroker(ABC):
    @abstractmethod
    def set_asset_to_trade(self, asset_to_trade: str):
        ...

    @abstractmethod
    def get_current_funds(self):
        ...

    @abstractmethod
    def get_asset_price(self):
        ...

    @abstractmethod
    def get_current_quantity(self):
        ...

    @abstractmethod
    def buy(self, quantity: int):
        ...

    @abstractmethod
    def sell(self, quantity: int):
        ...


class BuyTheClose:
    def __init__(self, trading_partner: TradingPartner):
        self.trading_broker: TradingBroker

        if trading_partner == TradingPartner.mock:
            self.trading_broker = MockTradingBroker()
        elif trading_partner == TradingPartner.zerodha:
            self.trading_broker = ZerodhaTradingBroker()

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

        quantity = current_funds // current_price

        self.trading_broker.buy(quantity)

    def sell(self):
        current_quantity = self.trading_broker.get_current_quantity()

        self.trading_broker.sell(current_quantity)


if __name__ == '__main__':
    BuyTheClose(TradingPartner.mock).run('NIFTYBEES', TradingDirection.long)
