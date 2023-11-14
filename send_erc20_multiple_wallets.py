from utils import wallet, web3, config
from contract import erc20
import csv


config_path = './files/config.json'

config_json = config.loadConfig(config_path)
rpc = config_json['rpc']
user_address = config_json['userAddress']
user_privite = config_json['userPirvateKey']

w3 = web3.build_web3(rpc)


from_wallet = wallet.Wallet(w3, user_address, user_privite)


erc20_usdt = erc20.ERC20(w3, '0x28cf872a62835aa77B8c2a6B508e78Be3fFc66aC')


print(erc20_usdt.balanceOf('0x920f15438788335689634D90e3Bb164544a904B5'))
print(erc20_usdt.balanceOfDivDecimals('0x920f15438788335689634D90e3Bb164544a904B5'))
print(erc20_usdt.totalSupply)
print(erc20_usdt.name)
print(erc20_usdt.decimals)

file_path = './files/wallets_1699867201.csv'

first_row = True
nonce = from_wallet.nonce()
with open(file_path) as f:
    reader = csv.reader(f)
    for row in reader:
        if first_row:
            first_row = False
            continue

        message = erc20_usdt.transfer(row[0], 20 * (10 ** erc20_usdt.decimals), from_wallet, nonce)
        nonce = nonce + 1
        print(message)

