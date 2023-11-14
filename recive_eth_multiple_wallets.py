from utils import wallet, web3, config
import csv

config_path = './files/config.json'

config_json = config.loadConfig(config_path)
rpc = config_json['rpc']

w3 = web3.build_web3(rpc)

file_path = './files/wallets_1699867201.csv'

first_row = True
with open(file_path) as f:
    reader = csv.reader(f)
    for row in reader:
        if first_row:
            first_row = False
            continue
        from_wallet = wallet.Wallet(w3, row[0], row[1])
        tx_hash,tmp = from_wallet.transferETHMax('0x920f15438788335689634D90e3Bb164544a904B5')
        print(tx_hash)
