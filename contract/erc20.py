
from web3 import Web3, HTTPProvider
import time
import json
from decimal import Decimal
from .abi import erc20_abi


class ERC20:
    def __init__(self, w3, tokenAddress):
        self.erc20_contract = w3.eth.contract(address=tokenAddress, abi=erc20_abi.ERC20_ABI)
        self.totalSupply = self.erc20_contract.functions.totalSupply().call()
        self.name = self.erc20_contract.functions.name().call()
        self.decimals = self.erc20_contract.functions.decimals().call()

    
    def transferFrom(self, sender, recipient, amount, wallet, nonce):
        try:
            sender = Web3.toChecksumAddress(sender)
            recipient = Web3.toChecksumAddress(recipient)

            if Decimal(self.balanceOf(sender)) < Decimal(amount):
                    return None, 'Platform USDT token is insufficient, please try again later'
            estimate_gas = self.erc20_contract.functions.transferFrom(sender, recipient, amount).estimateGas({'from':sender})
            approve_txn = self.erc20_contract.functions.transferFrom(sender, recipient, amount).buildTransaction(
                wallet.buildTx(estimate_gas, nonce)
            )
            tx_hash =  wallet.signedAndSendTransaction(tx = approve_txn)
            return tx_hash, 'success'

        except Exception as e:
            return None, str(e)


    def transfer(self, recipient, amount, wallet, nonce):
        try:
            sender = wallet.address()
            recipient = Web3.toChecksumAddress(recipient)

            if Decimal(self.balanceOf(sender)) < Decimal(amount):
                return None, 'Platform USDT token is insufficient, please try again later'
            # 进行转账代币

            estimate_gas = self.erc20_contract.functions.transfer(recipient, amount).estimateGas({'from':sender})
            txn = self.erc20_contract.functions.transfer(recipient, amount).buildTransaction(wallet.buildTx(estimate_gas, nonce))
            tx_hash = wallet.signedAndSendTransaction(txn)
            return tx_hash, 'success'
        except Exception as e:
            return None, str(e)

    def approve(self, spender, amount, wallet, nonce):
        try:
            spender = Web3.toChecksumAddress(spender)
            userAddress = wallet.address()
            estimate_gas = self.erc20_contract.functions.approve(spender, amount).estimateGas({'from':spender})
            approve_txn = self.erc20_contract.functions.approve(spender, amount).buildTransaction( wallet.buildTx(estimate_gas, nonce))
            tx_hash = wallet.signedAndSendTransaction(approve_txn)
            return tx_hash, 'success'
        except Exception as e:
            return None, str(e)

    def balanceOf(self, address):
        return self.erc20_contract.functions.balanceOf(address).call()

    def balanceOfDivDecimals(self, address):
        return self.balanceOf(address) / (10 ** self.decimals)


    def allowance(self, owner, spender):
        return self.erc20_contract.functions.allowance(owner, spender).call()

    
 








