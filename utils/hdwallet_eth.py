#!/usr/bin/env python3

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional



# 生成钱包和私钥，numbers 为生成的数量
# 返回值 
def  generate_hdwallet(numbers):
    # Generate english mnemonic words
    MNEMONIC: str = generate_mnemonic(language="english", strength=128)
    # Secret passphrase/password for mnemonic
    PASSPHRASE: Optional[str] = None  # "meherett"

    # Initialize Ethereum mainnet BIP44HDWallet
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    # Get Ethereum BIP44HDWallet from mnemonic
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    # Clean default BIP44 derivation indexes/paths
    bip44_hdwallet.clean_derivation()

    # print("Mnemonic:", bip44_hdwallet.mnemonic())
    # print("Base HD Path:  m/44'/60'/0'/0/{address_index}", "\n")

    wallet_list = []

    # Get Ethereum BIP44HDWallet information's from address index
    for address_index in range(numbers):
        # Derivation from Ethereum BIP44 derivation path
        bip44_derivation: BIP44Derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
        )
        # Drive Ethereum BIP44HDWallet
        bip44_hdwallet.from_path(path=bip44_derivation)
        # Print address_index, path, address and private_key
        # print(f"({address_index}) {bip44_hdwallet.path()} {bip44_hdwallet.address()} 0x{bip44_hdwallet.private_key()}")
        # Clean derivation indexes/paths
        wallet_list.append([bip44_hdwallet.address(), "0x" + bip44_hdwallet.private_key()])
        bip44_hdwallet.clean_derivation()

    
    return bip44_hdwallet.mnemonic(), wallet_list