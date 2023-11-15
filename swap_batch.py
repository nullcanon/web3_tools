from utils import wallet, web3, config
from contract import erc20, uniswapv2
import csv

config_path = './files/config.json'

config_json = config.loadConfig(config_path)
rpc = config_json['rpc']

user_address = config_json['userAddress']
user_privite = config_json['userPirvateKey']

w3 = web3.build_web3(rpc)


from_wallet = wallet.Wallet(w3, user_address, user_privite)
uniswap_v2 = uniswapv2.Uniswapv2(w3, '0xD99D1c33F9fC3444f8101754aBC46c52416550D1')

usdt = '0x28cf872a62835aa77B8c2a6B508e78Be3fFc66aC'
btc = '0xb02A8fd86fF3A2EAF85904a844dF995677f13509'

erc20_usdt = erc20.ERC20(w3, usdt)

file_path = './files/wallets_1699964700.csv'


first_row = True
with open(file_path) as f:
    reader = csv.reader(f)
    for row in reader:
        if first_row:
            first_row = False
            continue
        from_wallet = wallet.Wallet(w3, row[0], row[1])
        amount = 1 * (10 ** erc20_usdt.decimals)
        nonce = from_wallet.nonce()

        message = uniswap_v2.swapExactTokensForTokens([usdt,btc], 1 * (10 ** erc20_usdt.decimals), from_wallet, nonce)
        print(message)