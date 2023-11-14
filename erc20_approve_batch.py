from utils import wallet, web3, config
from contract import erc20, uniswapv2
import csv

config_path = './files/config.json'

config_json = config.loadConfig(config_path)
rpc = config_json['rpc']

w3 = web3.build_web3(rpc)

uniswap_v2 = uniswapv2.Uniswapv2(w3, '0xD99D1c33F9fC3444f8101754aBC46c52416550D1')

usdt = '0x28cf872a62835aa77B8c2a6B508e78Be3fFc66aC'
btc = '0xb02A8fd86fF3A2EAF85904a844dF995677f13509'

erc20_usdt = erc20.ERC20(w3, usdt)
erc20_btc = erc20.ERC20(w3, btc)

file_path = './files/wallets_1699867201.csv'

UINT256_MAX = 2**256-1

first_row = True
with open(file_path) as f:
    reader = csv.reader(f)
    for row in reader:
        if first_row:
            first_row = False
            continue
        from_wallet = wallet.Wallet(w3, row[0], row[1])
        nonce = from_wallet.nonce()
        approve_message_usdt = erc20_usdt.approve(uniswap_v2.routerAddress, UINT256_MAX, from_wallet, nonce)
        print(approve_message_usdt)

        approve_message_btc = erc20_btc.approve(uniswap_v2.routerAddress, UINT256_MAX, from_wallet, nonce + 1)
        print(approve_message_btc)


