from utils import hdwallet_eth
import csv
import time

mnemonic, wallets = hdwallet_eth.generate_hdwallet(10)

file_path = './files/wallets_' + str(int(time.time())) + '.csv'

with open(file_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([mnemonic])
    for wallet in wallets:
        newrow = []
        newrow.append(wallet[0])
        newrow.append(wallet[1])
        writer.writerow(newrow)