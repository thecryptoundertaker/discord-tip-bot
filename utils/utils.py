from loguru import logger
import math
from decimal import Decimal
from tokens.tokens import tokens
from config import config

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

@logger.catch
def get_min_gas(w3):
    gas_price = Decimal(config["GAS_PRICE"])
    gas_limit = Decimal(config["GAS_LIMIT"])
    return w3.fromWei(gas_price * gas_limit, "gwei") # enough for 1 tx

