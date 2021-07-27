import math
from decimal import Decimal
from tokens.tokens import tokens

def round_down(n, decimals=0):
    multiplier = Decimal(10 ** decimals)
    return math.floor(n * multiplier) / multiplier

def to_decimal(n, decimals=0):
    n = n * Decimal(f"1e{decimals}")
    return int(n)

def from_decimal(n, decimals=0):
    return n / Decimal(f"1e{decimals}")
