import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class TradingBroker(ABC):
    @abstractmethod
    def set_asset_to_trade(self, asset_to_trade: str) -> None:
        ...

    @abstractmethod
    def get_current_funds(self) -> float:
        ...

    @abstractmethod
    def get_asset_price(self) -> float:
        ...

    @abstractmethod
    def get_current_quantity(self) -> int:
        ...

    @abstractmethod
    def buy(self, quantity: int):
        ...

    @abstractmethod
    def sell(self, quantity: int):
        ...
