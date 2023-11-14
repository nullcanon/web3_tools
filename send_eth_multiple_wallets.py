from utils import wallet, web3, config
import csv

config_path = './files/config.json'

config_json = config.loadConfig(config_path)
rpc = config_json['rpc']

user_address = config_json['userAddress']
user_privite = config_json['userPirvateKey']

w3 = web3.build_web3(rpc)


from_wallet = wallet.Wallet(w3, user_address, user_privite)
file_path = './files/wallets_1699867201.csv'

first_row = True
nonce = from_wallet.nonce()
with open(file_path) as f:
    reader = csv.reader(f)
    for row in reader:
        if first_row:
            first_row = False
            continue

        tx_hash, tmp = from_wallet.transferETHWithNonce(row[0], 0.001, nonce)
        nonce = nonce + 1
        print(tx_hash)