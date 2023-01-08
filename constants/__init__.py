import logging
from enum import StrEnum

logger = logging.getLogger(__name__)


class TradingPartner(StrEnum):
    zerodha = 'zerodha'
    icici = 'icici'
    mock = 'mock'


class TradingDirection(StrEnum):
    long = 'long'
    short = 'short'
