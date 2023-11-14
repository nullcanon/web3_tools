from web3 import Web3, HTTPProvider
import time
import logging
import json
from decimal import Decimal
from .abi import uniswapv2_router_abi


class Uniswapv2:
    def __init__(self, w3, swapRouterAddress):
        self.routerAddress = swapRouterAddress
        self.uniswap_contract = w3.eth.contract(address=swapRouterAddress, abi=uniswapv2_router_abi.UNISWAPV2_ROUTER_ABI)

    def swapExactTokensForTokensSupportingFeeOnTransferTokens():
        pass

    def swapExactETHForTokensSupportingFeeOnTransferTokens():
        pass

    
    def swapExactTokensForETHSupportingFeeOnTransferTokens():
        pass

     # addressPath = [fromAddress, toAddress]
    def swapExactTokensForTokens(self, addressPath, fromAmount, wallet, nonce):
        user = wallet.address()
        estimate_gas = self.uniswap_contract.functions.swapExactTokensForTokens(
            fromAmount,
            0,
            addressPath,
            user,
            int(time.time()) + 2000
        ).estimateGas({'from':user})
        uniswap_txn = self.uniswap_contract.functions.swapExactTokensForTokens(
            fromAmount,
            0,
            addressPath,
            user,
            int(time.time()) + 2000
        ).buildTransaction(
            wallet.buildTx(int(estimate_gas * 1.2), nonce)
        )
        return wallet.signedAndSendTransaction(tx = uniswap_txn)

    def swapExactETHForTokens(self, addressPath, fromAmount, wallet, nonce):
        if fromAmount < 1000:
            return
        uniswap_contract = self.w3.eth.contract(address=swapRouterAddress, abi=self.uniswapV2Router02Abi)
        uniswap_txn = uniswap_contract.functions.swapExactETHForTokens(
            0,
            addressPath,
            # self.userAddress,
            self.toAddress,
            int(time.time()) + 100000000
        ).buildTransaction({
            'chainId': chainId,
            'nonce': self.w3.eth.get_transaction_count(self.userAddress),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei')
        })
        self.signedAndSendTransaction(tx = uniswap_txn)


    def addLiquidity(self, swapRouterAddress, tokenA, tokenB, tokenAAmount, tokenBAmount):
        if tokenAAmount < 1000 or tokenBAmount < 1000:
            return
        uniswap_contract = self.w3.eth.contract(address=swapRouterAddress, abi=self.uniswapV2Router02Abi)
        uniswap_txn = uniswap_contract.functions.addLiquidity(
            tokenA,
            tokenB,
            tokenAAmount,
            tokenBAmount,
            0,
            0,
            self.toAddress,
            int(time.time()) + 100000000
        ).buildTransaction({
            'chainId': chainId,
            'nonce': self.w3.eth.get_transaction_count(self.userAddress),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei')
        })
        self.signedAndSendAndWaitTransaction(tx = uniswap_txn)
        logging.info(self.userAddress + " addLiquidity success.")



    def addLiquidityETH(self, swapRouterAddress, tokenA, tokenB, tokenAAmount, tokenBAmount):
        if tokenAAmount < 1000 or tokenBAmount < 1000:
            return
        uniswap_contract = self.w3.eth.contract(address=swapRouterAddress, abi=self.uniswapV2Router02Abi)
        uniswap_txn = uniswap_contract.functions.addLiquidity(
            tokenA,
            tokenB,
            tokenAAmount,
            tokenBAmount,
            0,
            0,
            self.toAddress,
            int(time.time()) + 100000000
        ).buildTransaction({
            'chainId': chainId,
            'nonce': self.w3.eth.get_transaction_count(self.userAddress),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei')
        })
        self.signedAndSendAndWaitTransaction(tx = uniswap_txn)
        logging.info(self.userAddress + " addLiquidity success.")


    def getAmountsOut(self, amountIn,  In,  Out):
        if amountIn < 1000:
            return [0,0]
        uniswap_contract = self.w3.eth.contract(address=swapRouterAddress, abi=self.uniswapV2Router02Abi)
        return uniswap_contract.functions.getAmountsOut(amountIn, [In, Out]).call()

    def getAmountsIn(self, amountIn,  In,  Out):
        if amountIn < 1000:
            return [0,0]
        uniswap_contract = self.w3.eth.contract(address=swapRouterAddress, abi=self.uniswapV2Router02Abi)
        return uniswap_contract.functions.getAmountsIn(amountIn, [In, Out]).call()