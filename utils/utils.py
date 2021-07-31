from loguru import logger
import math
from decimal import Decimal
from tokens.tokens import tokens

@logger.catch
def to_lower(arg):
    return arg.lower()

@logger.catch
def round_down(n, decimals=0):
    multiplier = Decimal(10 ** decimals)
    return math.floor(n * multiplier) / multiplier

@logger.catch
def to_decimal(n, decimals=0):
    n = n * Decimal(f"1e{decimals}")
    return int(n)

@logger.catch
def from_decimal(n, decimals=0):
    return n / Decimal(f"1e{decimals}")
