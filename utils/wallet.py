
from web3 import Web3, HTTPProvider
from decimal import Decimal


class Wallet:
    def __init__(self, w3, userAddress, userPirvateKey):
        self.userAddress = Web3.toChecksumAddress(userAddress)
        self.userPirvateKey = userPirvateKey
        self.w3 = w3
        self.chain_id = self.w3.eth.chain_id
    

    def signedAndSendAndWaitTransaction(self, tx):
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=self.userPirvateKey)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return  self.w3.toHex(tx_hash)

    def signedAndSendTransaction(self, tx):
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=self.userPirvateKey)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return  self.w3.toHex(tx_hash)

    def buildTx(self, estimateGas, nonce):
        return {
                'from': self.userAddress,
                'nonce': nonce,
                'gas': estimateGas,
                'gasPrice': self.gasPrice(),
                'chainId': self.chain_id
            }


    def address(self):
        return self.userAddress

    def nonce(self):
        return self.w3.eth.get_transaction_count(self.userAddress)
    
    def ethAmount(self):
        return self.w3.fromWei(self.w3.eth.get_balance(self.userAddress), 'ether')

    def ethAmountWei(self):
        return self.w3.eth.get_balance(self.userAddress)

    def gasPrice(self):
        return self.w3.eth.gasPrice

    def chainID(self):
        return self.chain_id

    def __transferETH(self, toAddress, valueWei, nonce):
        try:
            # 如果代币不足返回异常
            if Decimal(self.ethAmountWei()) < Decimal(valueWei):
                return None, 'Platform ETH token is insufficient, please try again later'
            toAddress = Web3.toChecksumAddress(toAddress)
            tx = {
                'from': self.userAddress,
                'nonce': nonce,
                'to': toAddress,
                'gas': 21000,
                'gasPrice': self.gasPrice(),
                'value': valueWei,
                'chainId': self.chainID()
            }
            # 签名交易
            tx_hash = self.signedAndSendTransaction(tx)
            return tx_hash, 'pay success'
        except Exception as e:
            print(f'转账eth时发生异常：{e}')
            return None, str(e)

    
    def transferETHWithNonce(self, toAddress, value, nonce):
        return self.__transferETH(toAddress, Web3.toWei(value, 'ether'), nonce)



    def transferETH(self, toAddress, value):
        return self.__transferETH(toAddress, Web3.toWei(value, 'ether'), self.nonce())


    def transferETHMax(self, toAddress):
        valueWei = self.ethAmountWei() - 21000 * self.gasPrice()
        return self.__transferETH(toAddress, valueWei, self.nonce())
    