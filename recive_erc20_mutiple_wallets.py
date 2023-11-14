from utils import wallet, web3, config
from contract import erc20
import csv

config_path = './files/config.json'

config_json = config.loadConfig(config_path)
rpc = config_json['rpc']

w3 = web3.build_web3(rpc)

file_path = './files/wallets_1699867201.csv'
erc20_usdt = erc20.ERC20(w3, '0x28cf872a62835aa77B8c2a6B508e78Be3fFc66aC')

first_row = True
with open(file_path) as f:
    reader = csv.reader(f)
    for row in reader:
        if first_row:
            first_row = False
            continue
        from_wallet = wallet.Wallet(w3, row[0], row[1])
        message = erc20_usdt.transfer('0x920f15438788335689634D90e3Bb164544a904B5', 1 * (10 ** erc20_usdt.decimals), from_wallet, from_wallet.nonce())
        print(message)
