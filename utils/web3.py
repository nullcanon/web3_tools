
from web3 import Web3
from web3.middleware import geth_poa_middleware


def build_web3(provider):
    w3 = Web3(Web3.HTTPProvider(provider))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def get_eth_amount(w3, address):
    return w3.fromWei(w3.eth.get_balance(address), 'ether')