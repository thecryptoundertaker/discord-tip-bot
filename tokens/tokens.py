from frozendict import frozendict
import json

# utils

def get_token_abi(token):
    try:
        with open("tokens/abi/%s.json" % token['symbol'].lower()) as f:
            abi = json.load(f)
        return abi
    except:
        raise

# supported tokens

ftm = frozendict({
    "symbol": "FTM",
    "name": "Fantom",
    "decimals": 18
    })

usdc = frozendict({
    "contract_address": "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75",
    "type": "ERC20",
    "symbol": "USDC",
    "name": "USD Coin",
    "decimals": 6
    })

tbond = frozendict({
    "contract_address": "0x24248CD1747348bDC971a5395f4b3cd7feE94ea0",
    "type": "ERC20",
    "symbol": "TBOND",
    "name": "Tomb Bond",
    "decimals": 18
    })

tomb = frozendict({
    "contract_address": "0x6c021Ae822BEa943b2E66552bDe1D2696a53fbB7",
    "type": "ERC20",
    "symbol": "TOMB",
    "name": "Tomb",
    "decimals": 18
    })

tshare = frozendict({
    "contract_address": "0x4cdF39285D7Ca8eB3f090fDA0C069ba5F4145B37",
    "type": "ERC20",
    "symbol": "TSHARE",
    "name": "Tomb Share",
    "decimals": 18
    })

tokens = {
        "ftm": ftm,
        "usdc": usdc,
        "tbond": tbond,
        "tomb": tomb,
        "tshare": tshare
        }
