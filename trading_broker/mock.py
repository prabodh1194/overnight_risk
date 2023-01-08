import logging

from strategy.buy_the_close import TradingBroker

logger = logging.getLogger(__name__)


class MockTradingBroker(TradingBroker):
    ...