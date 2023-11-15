import csv
from utils import wallet, web3, config
from contract import erc20
from utils import hdwallet_eth
import time

def send_eth_bath(file_path, from_wallet, amount):
    first_row = True
    nonce = from_wallet.nonce()
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if first_row:
                first_row = False
                continue

            tx_hash, tmp = from_wallet.transferETHWithNonce(row[0], amount, nonce)
            nonce = nonce + 1
            print(tx_hash)




def recive_eth_batch(w3, file_path, recive_address):
    first_row = True
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if first_row:
                first_row = False
                continue
            from_wallet = wallet.Wallet(w3, row[0], row[1])
            tx_hash,tmp = from_wallet.transferETHMax(recive_address)
            print(tx_hash)




def send_erc20_batch(file_path, erc20_token, from_wallet):
    first_row = True
    nonce = from_wallet.nonce()
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if first_row:
                first_row = False
                continue

            message = erc20_token.transfer(row[0], 20 * (10 ** erc20_token.decimals), from_wallet, nonce)
            nonce = nonce + 1
            print(message)


def recive_erc20_batch(w3, file_path, erc20_token, recive_address):
    first_row = True
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if first_row:
                first_row = False
                continue
            from_wallet = wallet.Wallet(w3, row[0], row[1])
            message = erc20_token.transfer(recive_address, 1 * (10 ** erc20_token.decimals), from_wallet, from_wallet.nonce())
            print(message)


def generate_wallets_batch(numbers):
    mnemonic, wallets = hdwallet_eth.generate_hdwallet(numbers)

    file_name = 'wallets_' + str(int(time.time())) + '.csv'
    file_path = './files/' + file_name

    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([mnemonic])
        for wallet in wallets:
            newrow = []
            newrow.append(wallet[0])
            newrow.append(wallet[1])
            writer.writerow(newrow)

    return file_name, mnemonic, wallets